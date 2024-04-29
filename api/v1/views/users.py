#!/usr/bin/python3
"""User object that handles all default RESTFul API actions"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User
from api.v1.views.api_rest import API_rest


@app_views.route('/users', methods=['GET'])
def read_all_users():
    """Retrieves the list of all User objects"""
    return jsonify(API_rest.read_all(User))


@app_views.route('/users/<user_id>', methods=['GET'])
def read_user(user_id):
    """Retrieves a User object"""
    user = API_rest.read_by_id(User, user_id)
    if user.get('status code') == 404:
        abort(404)
    return jsonify(user.get('object dict'))


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Deletes a User object"""
    date_delete_response = API_rest.delete(User, user_id)
    if date_delete_response.get('status code') == 404:
        abort(404)
    return jsonify({})


@app_views.route('/users', methods=['POST'])
def create_user():
    """Creates a User"""
    date_from_request = request.get_json()
    if not date_from_request:
        return jsonify({'error': 'Not a JSON'}), 400
    if not date_from_request.get('email'):
        return jsonify({'error': 'Missing email'}), 400
    if not date_from_request.get('password'):
        return jsonify({'error': 'Missing password'}), 400
    date_user = User(**date_from_request)
    post_res = API_rest.create(date_user)
    return post_res.get('object dict'), post_res.get('status code')


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Updates a User object"""
    date_from_request = request.get_json()
    if not date_from_request:
        abort(400, "Not a JSON")

    ignored_arguments = ['id', 'created_at', 'updated_at', 'email']
    put_res = API_rest.update(
        User, user_id, ignored_arguments, date_from_request)
    if put_res.get('status code') == 404:
        abort(404)
    return put_res.get('object dict'), put_res.get('status code')
