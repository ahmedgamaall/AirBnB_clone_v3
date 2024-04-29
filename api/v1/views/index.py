#!/usr/bin/python3
"""app_views from api.v1.views"""
from flask import jsonify
from api.v1.views import app_views
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


@app_views.route('/status')
def status():
    """an endpoint that returns {"status": "OK"}"""
    return jsonify({"status": "OK"}), 200


@app_views.route('/stats')
def stats():
    """an endpoint that retrieves the number of each objects by type"""
    classes_dict = {"amenities": Amenity, "cities": City, "places": Place,
               "reviews": Review, "states": State, "users": User}
    counter_dict = {}
    for key, value in classes_dict.items():
        counter_dict[key] = storage.count(value)
    return jsonify(counter_dict)
