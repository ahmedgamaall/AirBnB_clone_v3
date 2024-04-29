#!/usr/bin/python3
"""Place objects and Amenity objects that handles all default RESTFul API"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity
from os import getenv


@app_views.route("/places/<place_id>/amenities", methods=['GET'])
def read_place_amenities(place_id):
    """Retrieves the list of all Amenity objects of a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenities_dict = list(map(lambda a: a.to_dict(), place.amenities))

    return jsonify(amenities_dict)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=['DELETE'])
def delete_place_amenity(place_id, amenity_id):
    """Deletes a Amenity object to a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    storage_t = getenv("HBNB_TYPE_STORAGE")
    if storage_t == "db":
        place_amenity = None
        for amenity in place.amenities:
            if amenity.id == amenity_id:
                place_amenity = amenity
                break
        if place_amenity is None:
            abort(404)
        storage.delete(place_amenity)
    else:
        try:
            place.amenity_ids.remove(amenity_id)
        except Exception as e:
            abort(404)
    storage.save()

    return jsonify({})


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=['POST'])
def create_place_amenity(place_id, amenity_id):
    """Link a Amenity object to a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage_t = getenv("HBNB_TYPE_STORAGE")
    status_code = 200
    if storage_t == "db":
        if amenity not in place.amenities:
            place.amenities.append(amenity)
            storage.save()
            status_code = 201
    else:
        if amenity_id not in place.amenity_ids:
            place.amenity_ids.append(amenity_id)
            storage.save()
            status_code = 201

    return jsonify(amenity.to_dict()), status_code
