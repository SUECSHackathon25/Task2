import os
from flask import Flask
from config import App
from task2.database import db, ma


def create_app():
    # create and configure the app
    app = Flask(__name__)

    app.config.from_object(App)
    

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app