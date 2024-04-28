#!/usr/bin/python3
"""app route named : app_views"""

from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status')
def status():
    """returns a JSON: "status": "OK"""""
    return jsonify({"status": "OK"})
