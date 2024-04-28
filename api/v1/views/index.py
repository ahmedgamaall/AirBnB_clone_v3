#!/usr/bin/python3
"""app route named : app_views"""

from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

@app_views.route('/status')
def status():
    """returns a JSON: "status": "OK"""""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def status():
    """an endpoint that retrieves the number of each objects"""""
    classes_data = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User"),
    }

    response = jsonify(classes_data)
    response.status_code = 200

    return response
