from flask import Flask, request, jsonify
from flask_restful import Resource, Api, abort
from models.convert import Convert
from webargs import fields, missing
from webargs.flaskparser import parser, abort, use_kwargs
from models.rates import Rates
from utils import daterange, format_to_dot_date, cnb_day, format_from_dot_date
import datetime


app = Flask(__name__)
api = Api(app)

settings = app.config.get('RESTFUL_JSON', {})
settings.setdefault('indent', 2)
settings.setdefault('sort_keys', True)
app.config['RESTFUL_JSON'] = settings

# Return validation errors as JSON for 422 and 400
@app.errorhandler(422)
@app.errorhandler(400)
def handle_error(err):
    messages = err.data.get("messages", ["Invalid request."])
    return jsonify({"Error": messages}), err.code


class ConversionRoute(Resource):
    @use_kwargs(
        {
            "input_currency": fields.Str(required=True),
            "amount": fields.Float(required=True, validate=lambda val: val > 0),
            "output_currency": fields.Str(required=False, missing="All"),
            "date": fields.Date(
                required=False,
                validate=lambda val: val >= datetime.date(1991, 1, 1),
                missing=None,
            ),
        }
    )
    def get(self, **kwargs):
        cnvrt = Convert(
            kwargs["input_currency"], kwargs["amount"], kwargs["output_currency"]
        )
        if kwargs["date"]:
            return cnvrt.convert(format_to_dot_date(cnb_day(kwargs["date"])))
        return cnvrt.convert(format_to_dot_date(cnb_day()))


class LatestRoute(Resource):
    @use_kwargs(
        {
            "base": fields.Str(required=False, missing="CZK"),
            "rates": fields.DelimitedList(
                fields.Str(), required=False, missing=["All"]
            ),
        }
    )
    def get(self, **kwargs):
        late = Rates(kwargs["base"], kwargs["rates"])
        if not late.base:
            return ({"Error": {"base": ["Unknown base currency or symbol."]}}, 400)
        if None in late.custom_list:
            return ({"Error": {"rates": ["Unknown rate currency or symbol."]}}, 400)
        date = format_to_dot_date(cnb_day())
        rates, date = late.fetch_rates(date)
        return {"base": late.base, "rates": {format_from_dot_date(date): rates}}


class HistoryRoute(Resource):
    @use_kwargs(
        {
            "date": fields.Date(
                required=False,
                validate=lambda val: val >= datetime.date(1991, 1, 1),
                missing=None,
            ),
            "start_date": fields.Date(
                required=False,
                validate=lambda val: val >= datetime.date(1991, 1, 1),
                missing=None,
            ),
            "end_date": fields.Date(
                required=False,
                validate=lambda val: val >= datetime.date(1991, 1, 1),
                missing=None,
            ),
        }
    )
    def get(self, **kwargs):
        if kwargs["date"] and not kwargs["start_date"] and not kwargs["end_date"]:
            singl_hist = Rates("CZK", ["All"])
            date = format_to_dot_date(cnb_day(kwargs["date"]))
            rates, date = singl_hist.fetch_rates(date)
            return {
                "base": "CZK",
                "rates": {kwargs['date'].strftime('%Y-%m-%d'): {format_from_dot_date(date): rates}
                },
            }

        elif not kwargs["date"] and kwargs["start_date"] and kwargs["end_date"]:
            out = {"base": "CZK", "rates": {}}
            multi_hist = Rates("CZK", ["All"])
            for dt in daterange(kwargs["start_date"], kwargs["end_date"]):
                one_day = format_to_dot_date(cnb_day(dt))
                rates, date = multi_hist.fetch_rates(one_day)
                out["rates"][format_from_dot_date(date)] = {dt.strftime('%Y-%m-%d'): rates}
            return out
        else:
            return ({"Error": {"dates": ["Ivalid input combination"]}}, 400)


api.add_resource(ConversionRoute, "/currency_converter")
api.add_resource(LatestRoute, "/latest")
api.add_resource(HistoryRoute, "/history")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
