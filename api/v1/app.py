#!/usr/bin/python3
"""flask app creation"""

from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify
from os import getenv
app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """method that close the storage"""
    storage.close()


@app.errorhandler(404)
def not_found(exception):
    """method that handles 404 error"""
    response_data = {
        "error": "Not found"
    }
    response = jsonify(response_data)
    response.status_code = 404

    return(response)


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", "5000")

    app.run(host=host, port=port, threaded=True)
