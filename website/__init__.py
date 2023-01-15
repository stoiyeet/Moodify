from flask import Flask
from os import path


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'

    from .apps import apps

    app.register_blueprint(apps, url_prefix='/')

    return app
