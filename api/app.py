from flask import Flask
from flask_restful import Resource, Api
import redis

app = Flask(__name__)
api = Api(app)

def get_hit_count():
        r.incr('hits')

r = redis.Redis(
    host='redis'
)
class Rates(Resource):
    def get(self):
        get_hit_count()
        return {'hello': int(r.get('hits'))}

api.add_resource(Rates, '/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)