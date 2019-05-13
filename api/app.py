from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from models.convert import Convert
from webargs import fields, missing
from webargs.flaskparser import parser, abort, use_kwargs
from models.latest import Latest
from models.history import History
import datetime


app = Flask(__name__)
api = Api(app)

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
        }
    )
    def get(self, **kwargs):
        cnvrt = Convert(
            kwargs["input_currency"], kwargs["amount"], kwargs["output_currency"]
        )
        return cnvrt.convert()


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
        late = Latest(kwargs["base"], kwargs["rates"])
        return late.fetch_rates()

class HistoryRoute(Resource):
    @use_kwargs(
        {
            "date": fields.Date(required=True, validate=lambda val: val >= datetime.date(1991, 1, 1)
            ),
        }
    )
    def get(self, **kwargs):
        hist = History(kwargs["date"])
        return hist.fetch_hist_rates()

api.add_resource(ConversionRoute, "/currency_converter")
api.add_resource(LatestRoute, "/latest")
api.add_resource(HistoryRoute, "/history")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
