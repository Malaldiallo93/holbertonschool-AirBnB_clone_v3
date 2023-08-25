#!/usr/bin/python3
"""
Route
"""

from api.v1.views import app_views, Amenity
from flask import jsonify, abort, request
from models import storage


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
def all_amenities():
    """ Method for the "/amenities" path GET
    Returns all amenities
    """
    amenities = storage.all(Amenity)
    amenities = [amenity.to_dict() for amenity in amenities.values()]
    return jsonify(amenities), 200


@app_views.route('/amenities/<id>', strict_slashes=False, methods=['GET'])
def get_amenity(id):
    """ Method for the "/amenities/<id>" path GET
    Returns amenity by id
    """
    amenity = storage.get(Amenity, id)
    if amenity:
        amenity = amenity.to_dict()
        return jsonify(amenity), 200
    return abort(404)


@app_views.route('/amenities/<id>', strict_slashes=False, methods=['DELETE'])
def delete_amenity(id):
    """Removes amenity by id"""
    amenity = storage.get(Amenity, id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    return abort(404)


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def create_amenity():
    """Creates a new amenity"""
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'name' in body:
        new_amenity = Amenity(**body)
        storage.new(new_amenity)
        storage.save()
        return jsonify(new_amenity.to_dict()), 201
    else:
        return jsonify({'error': 'Missing name'}), 400


@app_views.route('/amenities/<id>', strict_slashes=False, methods=['PUT'])
def update_amenity(id):
    """Updates an amenity"""
    amenity = storage.get(Amenity, id)
    if amenity:
        body = request.get_json(silent=True)
        if body is None:
            return jsonify({'error': 'Not a JSON'}), 400
        for key in body:
            if key != 'id' and key != 'created_at' and key != 'updated_at':
                setattr(amenity, key, body[key])
        amenity.save()
        return jsonify(amenity.to_dict()), 200
    return abort(404)
