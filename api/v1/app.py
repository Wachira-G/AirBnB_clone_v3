#!/usr/bin/python3
"""This is the app file for the api"""

from flask import Flask
from os import getenv
from models import storage
from api.v1.views import app_views


# def create_app():
app = Flask(__name__, )
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


if __name__ == "__main__":
    app.run(
            host=getenv('HBNB_API_HOST', '0.0.0.0'),
            port=getenv('HBNB_API_PORT', 5000),
            threaded=True,
            )