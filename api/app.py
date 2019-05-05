from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from convert import Convert
from webargs import fields, missing
from webargs.flaskparser import parser, abort, use_kwargs

app = Flask(__name__)
api = Api(app)

# Return validation errors as JSON for 422 and 400
@app.errorhandler(422)
@app.errorhandler(400)
def handle_error(err):
    headers = err.data.get("headers", None)
    messages = err.data.get("messages", ["Invalid request."])
    if headers:
        return jsonify({"errors": messages}), err.code, headers
    else:
        return jsonify({"errors": messages}), err.code


class Rates(Resource):

    @use_kwargs({'input_currency': fields.Str(required=True), 'amount': fields.Float(required=True), 'output_currency': fields.Str(required=False, missing='All')})
    def get(self, **kwargs):
        cnvrt = Convert(kwargs['input_currency'], kwargs['amount'], kwargs['output_currency'])
        return cnvrt.convert()

api.add_resource(Rates, '/currency_converter')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
