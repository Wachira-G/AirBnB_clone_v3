#!/usr/bin/python3
"""Handles all deflault RESTFul API actions for reviews."""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.review import Review
from werkzeug.exceptions import NotFound


@app_views.route("/reviews", methods=["GET"], strict_slashes=False)
def get_reviews():
    """Retrieve Review objects."""
    reviews = storage.all("Review")
    json_reviews = jsonify([review.to_dict() for review in reviews.values()])

    return json_reviews, 200


@app_views.route("/reviews/<string:id>", methods=["GET"], strict_slashes=False)
def get_a_review(id):
    """Retrieve a specific review object."""
    review = storage.get('Review', id)
    if review:
        json_review = jsonify(review.to_dict())
        return json_review, 200
    abort(404)


@app_views.route(
        "/reviews/<string:id>",
        methods=["DELETE"],
        strict_slashes=False,
        )
def delete_a_review(id):
    """Delete a specific review object."""
    review = storage.get('Review', id)
    if review:
        review.delete()
        storage.save()
        return {}, 200
    abort(404)


@app_views.route('/reviews/', methods=['POST'], strict_slashes=False)
def post_a_review():
    """Create a review object."""
    review_info = request.get_json()
    if review_info:
        if not review_info.get('name'):
            abort(400, 'Missing name')
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
        # filter out attrs
        IGNORE = ['__class__', 'id', 'created_at', 'update_at']
        review_dict = {k: v for k, v in review_dict.items() if k not in IGNORE}
        # review = Review(**review_dict)
        for key, value in review_dict.items():
            setattr(review, key, value)

        review.save()
        storage.new(review)
        storage.save()
        return jsonify(review.to_dict()), 200
    abort(400, 'Not a JSON')
