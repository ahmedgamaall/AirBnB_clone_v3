#!/usr/bin/python3
"""instance of Flask"""
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """close storage"""
    storage.close()


@app.errorhandler(404)
def page_not_found(exception):
    """a handler for 404 errors that returns a
    JSON-formatted 404 status code response"""
    error = {"error": "Not found"}
    status_code = 404
    return jsonify(error), status_code


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', 5000)
    app.run(host=host, port=port, threaded=True)
