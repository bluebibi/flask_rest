#https://flask-restful.readthedocs.io/en/latest/

from flask import Flask, render_template, request
from flask_restful import Api
import logging

from news import news_blueprint
from rest_server.resource_check import resource_blueprint
from rest_server.resource import TemperatureResource, TemperatureCreationResource, TemperatureByLocationResource

application = Flask(__name__)
application.register_blueprint(news_blueprint, url_prefix='/news')
application.register_blueprint(resource_blueprint, url_prefix='/resource')

api = Api(application)
api.add_resource(TemperatureResource, "/resource/<sensor_id>")
api.add_resource(TemperatureCreationResource, "/resource/creation")
api.add_resource(TemperatureByLocationResource, "/resource/location/<location>")

logging.basicConfig(
    filename='test.log',
    level=logging.DEBUG
)


@application.route('/')
def hello_html():
    value = 50
    value_list = ['파이썬', '자바', '스위프트']
    return render_template(
        'index.html',
        name="yhhan",
        value_list=value_list,
        value=value
    )


if __name__ == "__main__":
    logging.info("Flask Web Server Started!!!")

    application.debug = True
    application.config['DEBUG'] = True

    application.run(host="localhost", port="8080")