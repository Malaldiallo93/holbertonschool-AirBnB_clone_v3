#!/usr/bin/python3
"""
Route Places
"""

from api.v1.views import app_views, Place, City, User
from flask import jsonify, abort, request
from models import storage


@app_views.route('/cities/<id>/places', strict_slashes=False, methods=['GET'])
def get_city_place(id):
    """ Method for the "/cities/<id>/places" path GET
    Returns all Place objects in a City
    """
    city = storage.get(City, id)
    if city:
        places = [place.to_dict() for place in city.places]
        return jsonify(places), 200
    return abort(404)


@app_views.route('/places/<id>', strict_slashes=False, methods=['GET'])
def get_place(id):
    """ Method for the "/places/<id>" path GET
    Returns Place by id
    """
    place = storage.get(Place, id)
    if place:
        place = place.to_dict()
        return jsonify(place), 200
    return abort(404)


@app_views.route('/places/<id>', strict_slashes=False, methods=['DELETE'])
def delete_place(id):
    """Removes place by id"""
    place = storage.get(Place, id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    return abort(404)


@app_views.route('/cities/<id>/places', strict_slashes=False, methods=['POST'])
def create_place(id):
    """Creates a new place"""
    city_exist = storage.get(City, id)
    if city_exist is None:
        return abort(404)
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'user_id' not in body:
        return jsonify({'error': 'Missing user_id'}), 400
    user_exist = storage.get(User, body['user_id'])
    if user_exist is None:
        return abort(404)
    if 'name' not in body:
        return jsonify({'error': 'Missing name'}), 400
    new_place = Place(**body)
    setattr(new_place, 'city_id', id)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<id>', strict_slashes=False, methods=['PUT'])
def update_place(id):
    """Updates a place"""
    place = storage.get(Place, id)
    if place:
        body = request.get_json(silent=True)
        if body is None:
            return jsonify({'error': 'Not a JSON'}), 400
        if 'user_id' in body:
            user_exist = storage.get(User, body['user_id'])
            if user_exist is None:
                return abort(404)
        for key in body:
            if key != 'id' and key != 'created_at' and key != 'updated_at'\
                    and key != 'user_id' and key != 'city_id':
                setattr(place, key, body[key])
        place.save()
        return jsonify(place.to_dict()), 200
    return abort(404)
