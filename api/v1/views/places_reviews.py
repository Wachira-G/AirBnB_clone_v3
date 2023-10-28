#!/usr/bin/python3
"""Handles all deflault RESTFul API actions for reviews."""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.review import Review
from werkzeug.exceptions import NotFound


@app_views.route(
        "/places/<string:place_id>/reviews",
        methods=["GET"], strict_slashes=False)
def get_reviews(place_id):
    """Retrieve Review objects of a place."""
    place = storage.get('Place', place_id)
    if not place:
        abort(404)
    reviews = storage.all("Review")
    json_reviews = jsonify([
        review.to_dict() for review in reviews.values()
        if review.place_id == place_id])

    return json_reviews, 200


@app_views.route(
        "/reviews/<string:review_id>", methods=["GET"], strict_slashes=False)
def get_a_review(review_id):
    """Retrieve a specific review object."""
    review = storage.get('Review', review_id)
    if review:
        json_review = jsonify(review.to_dict())
        return json_review, 200
    abort(404)


@app_views.route(
        "/reviews/<string:review_id>",
        methods=["DELETE"],
        strict_slashes=False,
        )
def delete_a_review(review_id):
    """Delete a specific review object."""
    review = storage.get('Review', review_id)
    if review:
        review.delete()
        storage.save()
        return {}, 200
    abort(404)


@app_views.route(
        '/places/<string:place_id>/reviews/',
        methods=['POST'], strict_slashes=False
        )
def post_a_review(place_id):
    """Create a review object."""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    review_info = request.get_json()
    if review_info:
        user_id = review_info.get('user_id')
        if not user_id:
            abort(400, 'Missing user_id')
        if not storage.get("User", user_id):
            abort(404)
        if not review_info.get('text'):
            abort(400, 'Missing text')
        review_info.update({"place_id": place_id, "user_id": user_id})
        review = Review(**review_info)
        storage.new(review)
        storage.save()
        return jsonify(review.to_dict()), 201
    abort(400, 'Not a JSON')


@app_views.route('/reviews/<string:id>', methods=['PUT'], strict_slashes=False)
def put_a_review(id):
    """Update a review object."""
    review_info = request.get_json()
    if not review_info:
        abort(404)
    review = storage.get('Review', id)
    if review:
        review_dict = review.to_dict()
        review_dict.update(review_info)
        IGNORE = [
                '__class__', 'id', 'user_id', 'place_id',
                'created_at', 'updated_at',
                ]
        review_dict = {
                k: v for k, v in review_dict.items() if k not in IGNORE
                }
        for key, value in review_dict.items():
            setattr(review, key, value)

        review.save()
        storage.new(review)
        storage.save()
        return jsonify(review.to_dict()), 200
    abort(400, 'Not a JSON')
