#https://flask-restful.readthedocs.io/en/latest/
import os

from flask import Flask, render_template, session
from flask_oauthlib.client import OAuth
from flask_restful import Api
import logging

from database import base
from database.base import User
from views.news import news_blueprint
from views.auth import auth_blueprint
from rest_server.resource_check import resource_blueprint
from rest_server.resource import TemperatureResource, TemperatureCreationResource, TemperatureByLocationResource

from flask_login import current_user, LoginManager

application = Flask(__name__)
application.debug = True
application.register_blueprint(news_blueprint, url_prefix='/news')
application.register_blueprint(auth_blueprint, url_prefix='/auth')
application.register_blueprint(resource_blueprint, url_prefix='/resource')

api = Api(application)
api.add_resource(TemperatureResource, "/resource/<sensor_id>")
api.add_resource(TemperatureCreationResource, "/resource/creation")
api.add_resource(TemperatureByLocationResource, "/resource/location/<location>")

application.config['WTF_CSRF_SECRET_KEY'] = os.urandom(24)
application.config['SECRET_KEY'] = os.urandom(24)

login_manager = LoginManager()
login_manager.init_app(application)

logging.basicConfig(
    filename='test.log',
    level=logging.DEBUG
)

application.secret_key = 'development'
oauth = OAuth(application)
github = oauth.remote_app(
    name='github',
    consumer_key='a11a1bda412d928fb39a',
    consumer_secret='92b7cf30bc42c49d589a10372c3f9ff3bb310037',
    request_token_params={'scope': 'user:email'},
    base_url='https://api.github.com/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize'
)

@login_manager.user_loader
def load_user(user_id):
    q = base.db_session.query(User).filter(User.id == user_id)
    user = q.first()

    if user is not None:
        user._authenticated = True
    return user


@application.route('/')
def hello_html():
    value = 50
    value_list = ['파이썬', '자바', '스위프트']

    return render_template(
        'index.html',
        name="yhhan",
        value_list=value_list,
        value=value,
        current_user=current_user
    )


if __name__ == "__main__":
    logging.info("Flask Web Server Started!!!")

    application.debug = True
    application.config['DEBUG'] = True

    application.run(host="0.0.0.0", port="8080")