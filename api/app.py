from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from convert import Convert
from webargs import fields, missing
from webargs.flaskparser import parser, abort, use_kwargs


app = Flask(__name__)
api = Api(app)

class Rates(Resource):

    @use_kwargs({'input_currency': fields.Str(required=True), 'amount': fields.Float(required=True), 'output_currency': fields.Str(required=False, missing=None)})
    def get(self, **kwargs):
        cnvrt = Convert(kwargs['input_currency'], kwargs['amount'], kwargs['output_currency'])
        return cnvrt.convert()

api.add_resource(Rates, '/currency_converter')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
