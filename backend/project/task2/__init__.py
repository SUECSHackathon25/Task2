import os

from flask import Flask
from config import Config


def create_app():
    
    
    # create and configure the app
    app = Flask(__name__)
    

    app.config.from_object(Config)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app