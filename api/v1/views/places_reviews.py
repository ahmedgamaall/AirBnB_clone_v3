#!/usr/bin/python3"
"""Review object that handles all default RESTFul API actions"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User
from models.place import Place
from models.city import City
from models.review import Review
from api.v1.views.api_rest import API_rest


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def read_all_reviews(place_id):
    """Retrieves the list of all Review objects of a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = list(map(lambda review: review.to_dict(), place.reviews))
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def read_review(review_id):
    """Retrieves a Review object"""
    review = API_rest.read_by_id(Review, review_id)
    if review.get('status code') == 404:
        abort(404)
    return jsonify(review.get('object dict'))


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """Deletes a Review object"""
    date_delete_response = API_rest.delete(Review, review_id)
    if date_delete_response.get('status code') == 404:
        abort(404)
    return jsonify({})


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    """Creates a Review"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    date_from_request = request.get_json()
    if date_from_request is None:
        return jsonify({'error': 'Not a JSON'}), 400
    if not date_from_request.get('user_id'):
        return jsonify({'error': 'Missing user_id'}), 400
    if not date_from_request.get('text'):
        return jsonify({'error': 'Missing text'}), 400
    user = storage.get(User, date_from_request.get('user_id'))
    if user is None:
        abort(404)
    date_review = Review(text=date_from_request.get('text'), user_id=user.id,
                        place_id=place_id)
    post_from_response = API_rest.create(date_review)
    return post_from_response.get('object dict'), post_from_response.get('status code')


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """Updates a Review object"""
    date_from_request = request.get_json()
    if not date_from_request:
        return jsonify({'error': 'Not a JSON'}), 400

    ignored_arguments = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    put_from_response = API_rest.update(
        Review, review_id, ignored_arguments, date_from_request)
    if put_from_response.get('status code') == 404:
        abort(404)
    return put_from_response.get('object dict'), put_from_response.get('status code')
