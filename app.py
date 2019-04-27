from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class Rates(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(Rates, '/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)