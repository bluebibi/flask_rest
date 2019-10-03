#https://flask-restful.readthedocs.io/en/latest/

from flask import Flask
from flask_restful import Api

from rest_server.resource_check import resource_blueprint
from rest_server.resource import TemperatureResource, TemperatureCreationResource

application = Flask(__name__)
application.register_blueprint(resource_blueprint)
api = Api(application)


@application.route("/")
def say_hello(username="World"):
    return '<p>Hello {0}!</p>'.format(username)


api.add_resource(TemperatureResource, "/resource/<sensor_id>")
api.add_resource(TemperatureCreationResource, "/resource_creation")


if __name__ == "__main__":
    application.debug = True
    application.run()