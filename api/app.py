import redis
from flask import Flask
from flask_restful import Resource, Api
from convert import Convert


app = Flask(__name__)
api = Api(app)

r = redis.Redis(
    host='redis', decode_responses=True
    )

class Rates(Resource):
    def get(self):
        Convert.get_hit_count(r)
        cnvrt = Convert()
        return {'hello': 'data'}

api.add_resource(Rates, '/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)