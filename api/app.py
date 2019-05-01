from flask import Flask, request
from flask_restful import Resource, Api
from convert import Convert


app = Flask(__name__)
api = Api(app)

class Rates(Resource):
    def get(self):
        input_cur = request.args.get('input_currency')
        output_cur = request.args.get('output_currency', default=None)
        amount = request.args.get('amount', type=float)
        cnvrt = Convert(input_cur,amount,output_cur)
        return cnvrt.convert()

api.add_resource(Rates, '/currency_converter')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)