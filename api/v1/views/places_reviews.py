#!/usr/bin/python3
"""
Script for the cities API RESTful API
"""
from api.v1.views import app_views, Place, Review, User
from flask import jsonify, abort, request
from models import storage


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['GET'])
def get_reviews_places(place_id):
    """ Method for the "/places/<place_id>/reviews" path GET
    Returns reviews by place
    """
    place = storage.get(Place, place_id)
    if place:
        reviews = [review.to_dict() for review in place.reviews]
        return jsonify(reviews), 200
    return abort(404)


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['GET'])
def get_review(review_id):
    """ Method for the "/reviews/<review_id>" path GET
    Returns Review by id
    """
    review = storage.get(Review, review_id)
    if review:
        review = review.to_dict()
        return jsonify(review), 200
    return abort(404)


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_review(review_id):
    """Removes place by id"""
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    return abort(404)


@app_views.route('/places/<places_id>/reviews', strict_slashes=False,
                 methods=['POST'])
def create_review(places_id):
    """Creates a new place"""
    place = storage.get(Place, places_id)
    if not bool(place):
        return abort(404)

    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'error': 'Not a JSON'}), 400

    if 'user_id' not in body:
        return jsonify({'error': 'Missing user_id'}), 400
    user = storage.get(User, body.get('user_id'))
    if not bool(user):
        return abort(404)

    if 'text' in body:
        new_review = Review(**body)
        setattr(new_review, 'place_id', place.id)
        storage.new(new_review)
        storage.save()
        return jsonify(new_review.to_dict()), 201
    else:
        return jsonify({'error': 'Missing text'}), 400


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['PUT'])
def update_review(review_id):
    """Updates a place"""
    review = storage.get(Review, review_id)
    if review:
        body = request.get_json(silent=True)
        if body is None:
            return jsonify({'error': 'Not a JSON'}), 400
        for key in body:
            if key != 'id' and key != 'user_id' and key != 'place_id'\
                    and key != 'created_at' and key != 'updated_at':
                setattr(review, key, body.get(key))
        review.save()
        return jsonify(review.to_dict()), 200
    return abort(404)
