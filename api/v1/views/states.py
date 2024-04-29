#!/usr/bin/python3
"""State objects that handles all default RESTFul API actions"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from api.v1.views.api_rest import API_rest


@app_views.route('/states', methods=['GET'])
def read_all_states():
    """Retrieves the list of all State objects"""
    return jsonify(API_rest.read_all(State))


@app_views.route('/states/<state_id>', methods=['GET'])
def read_state(state_id):
    """Retrieves a State object"""
    state = API_rest.read_by_id(State, state_id)
    if state.get('status code') == 404:
        abort(404)
    return jsonify(state.get('object dict'))


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Deletes a State object"""
    date_delete_response = API_rest.delete(State, state_id)
    if date_delete_response.get('status code') == 404:
        abort(404)
    return jsonify({})


@app_views.route('/states', methods=['POST'])
def create_state():
    """Creates a State"""
    date_from_request = request.get_json()
    if not date_from_request:
        abort(400, "Not a JSON")
    if not date_from_request.get('name'):
        abort(400, "Missing name")
    date_state = State(name=date_from_request.get('name'))
    post_from_response = API_rest.create(date_state)
    return post_from_response.get('object dict'), post_from_response.get('status code')


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """Updates a State object"""
    date_from_request = request.get_json()
    if not date_from_request:
        return jsonify({'error': 'Not a JSON'}), 400

    ignored_arguments = ['id', 'created_at', 'updated_at']
    put_from_response = API_rest.update(
        State, state_id, ignored_arguments, date_from_request)
    if put_from_response.get('status code') == 404:
        abort(404)
    return put_from_response.get('object dict'), put_from_response.get('status code')
