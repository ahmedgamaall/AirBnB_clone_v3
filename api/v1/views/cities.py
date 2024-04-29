#!/usr/bin/python3
"""City objects that handles all default RESTFul API actions"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from api.v1.views.api_rest import API_rest


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def read_all_city(state_id):
    """Retrieves the list of all City objects of a State"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = list(map(lambda city: city.to_dict(), state.cities))
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'])
def read_city(city_id):
    """Retrieves a City object"""
    city = API_rest.read_by_id(City, city_id)
    if city.get('status code') == 404:
        abort(404)
    return jsonify(city.get('object dict'))


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """Deletes a City object"""
    date_delete_response = API_rest.delete(City, city_id)
    if date_delete_response.get('status code') == 404:
        abort(404)
    return jsonify({})


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """Creates a City"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    date_from_request = request.get_json()

    if date_from_request is None:
        abort(400, "Not a JSON")
    if not date_from_request.get('name'):
        abort(400, "Missing name")
    date_city = City(name=date_from_request.get('name'), state_id=state_id)
    post_from_response = API_rest.create(date_city)
    return post_from_response.get('object dict'), post_from_response.get('status code')


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """Updates a City object"""
    date_from_request = request.get_json()
    if not date_from_request:
        abort(400, "Not a JSON")

    ignored_arguments = ['id', 'created_at', 'updated_at']
    put_from_response = API_rest.update(
        City, city_id, ignored_arguments, date_from_request)
    if put_from_response.get('status code') == 404:
        abort(404)
    return put_from_response.get('object dict'), put_from_response.get('status code')
