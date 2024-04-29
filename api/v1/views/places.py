#!/usr/bin/python3
"""Place objects that handles all default RESTFul API actions"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User
from models.place import Place
from models.city import City
from models.state import State
from api.v1.views.api_rest import API_rest
from os import getenv


@app_views.route('/places/<place_id>', methods=['GET'])
def read_place(place_id):
    """Retrieves a Place object"""
    place = API_rest.read_by_id(Place, place_id)
    if place.get('status code') == 404:
        abort(404)
    return jsonify(place.get('object dict'))


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def read_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = list(map(lambda place: place.to_dict(), city.places))
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """Deletes a Place object"""
    date_delete_response = API_rest.delete(Place, place_id)
    if date_delete_response.get('status code') == 404:
        abort(404)
    return jsonify({})


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """Creates a Place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    date_from_request = request.get_json()
    if date_from_request is None:
        return jsonify({'error': 'Not a JSON'}), 400
    if not date_from_request.get('user_id'):
        return jsonify({'error': 'Missing user_id'}), 400
    if not date_from_request.get('name'):
        return jsonify({'error': 'Missing name'}), 400
    user = storage.get(User, date_from_request.get('user_id'))
    if user is None:
        abort(404)
    date_place = Place(name=date_from_request.get('name'), user_id=user.id,
                       city_id=city_id)
    post_resp = API_rest.create(date_place)
    return post_resp.get('object dict'), post_resp.get('status code')


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """Updates a Place object"""
    date_from_request = request.get_json()
    if not date_from_request:
        abort(400, "Not a JSON")
    ignored_args = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    put_resp = API_rest.update(
        Place, place_id, ignored_args, date_from_request)
    if put_resp.get('status code') == 404:
        abort(404)
    return put_resp.get('object dict'), put_resp.get('status code')


@app_views.route('/places_search', methods=['POST'])
def search_places():
    """Place objects depending of the JSON in the body of the request"""

    date_from_request = request.get_json()
    if date_from_request is None:
        return jsonify({'error': 'Not a JSON'}), 400

    states_data = date_from_request.get('states', [])
    cities_data = date_from_request.get('cities', [])
    amenities_data = date_from_request.get('amenities', [])

    if date_from_request == {} or (states_data == [] and
                                   cities_data == [] and amenities_data == []):
        all_places = storage.all(Place)
        all_places_list = list(map(lambda p: p.to_dict(), all_places.values()))
        return jsonify(all_places_list)

    places = []
    if states_data == [] and cities_data == []:
        places = list(map(lambda p: p, storage.all(Place).values()))
    else:
        for state_id in states_data:
            state = storage.get(State, state_id)
            if state:
                for city in state.cities:
                    places.extend(city.places)
        for city_id in cities_data:
            city = storage.get(City, city_id)
            if city:
                places.extend(city.places)
    places = list(set(places))
    if amenities_data:
        places_with_amenities = []
        for place in places:
            if getenv("HBNB_TYPE_STORAGE") == "db":
                if all(list(map(lambda a: a in
                                list(map(lambda c: c.id, place.amenities)),
                                amenities_data))):
                    del place.amenities
                    places_with_amenities.append(place.to_dict())
            else:
                if all(list(map(lambda a: a in place.amenities,
                                amenities_data))):
                    del place.amenities
                    places_with_amenities.append(place.to_dict())
        return jsonify(places_with_amenities)
    else:
        places_list = list(map(lambda p: p.to_dict(), places))
        return jsonify(places_list)
