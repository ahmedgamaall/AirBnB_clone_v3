#!/usr/bin/python3
"""Amenity objects that handles all default RESTFul API actions"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from api.v1.views.api_rest import API_rest


@app_views.route('/amenities', methods=['GET'])
def read_all_amenities():
    """Retrieves the list of all Amenity objects"""
    amenities = API_rest.read_all(Amenity)
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def read_amenity(amenity_id):
    """Retrieves a Amenity object"""
    amenity = API_rest.read_by_id(Amenity, amenity_id)
    if amenity.get('status code') == 404:
        abort(404)
    return jsonify(amenity.get('object dict'))


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """Deletes a Amenity object"""
    date_delete_response = API_rest.delete(Amenity, amenity_id)
    if date_delete_response.get('status code') == 404:
        abort(404)
    return jsonify({})


@app_views.route('/amenities', methods=['POST'])
def create_amenity():
    """Creates a Amenity"""
    date_from_request = request.get_json()
    if not date_from_request:
        return jsonify({'error': 'Not a JSON'}), 400
    if not date_from_request.get('name'):
        return jsonify({'error': 'Missing name'}), 400
    date_amenity = Amenity(name=date_from_request.get('name'))
    post_from_response = API_rest.create(date_amenity)
    return post_from_response.get('object dict'), post_from_response.get('status code')


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """Updates a Amenity object"""
    date_from_request = request.get_json()
    if not date_from_request:
        abort(400, "Not a JSON")

    ignored_arguments = ['id', 'created_at', 'updated_at']
    put_from_response = API_rest.update(
        Amenity, amenity_id, ignored_arguments, date_from_request)
    if put_from_response.get('status code') == 404:
        abort(404)
    return put_from_response.get('object dict'), put_from_response.get('status code')
