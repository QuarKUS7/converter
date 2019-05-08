from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from convert import Convert
from webargs import fields, missing
from webargs.flaskparser import parser, abort, use_kwargs
from latest import Latest


app = Flask(__name__)
api = Api(app)

# Return validation errors as JSON for 422 and 400
@app.errorhandler(422)
@app.errorhandler(400)
def handle_error(err):
    messages = err.data.get("messages", ["Invalid request."])
    return jsonify({"Error": messages}), err.code


class Conversion(Resource):
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

class Latest(Resource):
    @use_kwargs(
        {
            "base": fields.Str(required=False, missing=None),
            "rates": fields.Str(required=False, missing=None),
        }
    )
    def get(self, **kwargs):
        late = Latest(
            kwargs["base"], kwargs["rates"]
        )
        return late.fetch_rates()


api.add_resource(Conversion, "/currency_converter")
api.add_resource(Latest, "/latest")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
