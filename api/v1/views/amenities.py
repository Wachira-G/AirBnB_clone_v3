#!/usr/bin/python3
"""Handles all deflault RESTFul API actions for amenities."""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.amenity import Amenity
from werkzeug.exceptions import NotFound


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def get_amenities():
    """Retrieve Amenity objects."""
    amenities = storage.all("Amenity")
    json_amenities = jsonify([amenity.to_dict()
                              for amenity in amenities.values()])

    return json_amenities, 200


@app_views.route(
        "/amenities/<string:id>", methods=["GET"], strict_slashes=False)
def get_a_amenity(id):
    """Retrieve a specific amenity object."""
    amenity = storage.get('Amenity', id)
    if amenity:
        json_amenity = jsonify(amenity.to_dict())
        return json_amenity, 200
    abort(404)


@app_views.route(
        "/amenities/<string:id>",
        methods=["DELETE"],
        strict_slashes=False,
        )
def delete_a_amenity(id):
    """Delete a specific amenity object."""
    amenity = storage.get('Amenity', id)
    if amenity:
        amenity.delete()
        storage.save()
        return {}, 200
    abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_a_amenity():
    """Create a amenity object."""
    amenity_info = request.get_json()
    if amenity_info:
        if not amenity_info.get('name'):
            abort(400, 'Missing name')
        amenity = Amenity(**amenity_info)
        storage.new(amenity)
        storage.save()
        return jsonify(amenity.to_dict()), 201
    abort(400, 'Not a JSON')


@app_views.route(
        '/amenities/<string:id>', methods=['PUT'], strict_slashes=False)
def put_a_amenity(id):
    """Update a amenity object."""
    amenity_info = request.get_json()
    if not amenity_info:
        abort(404)
    amenity = storage.get('Amenity', id)
    if amenity:
        amenity_dict = amenity.to_dict()
        amenity_dict.update(amenity_info)
        # filter out attrs
        IGNORE = ['__class__', 'id', 'created_at', 'updated_at']
        amenity_dict = {
            k: v for k, v in amenity_dict.items() if k not in IGNORE}
        # amenity = Amenity(**amenity_dict)
        for key, value in amenity_dict.items():
            setattr(amenity, key, value)

        amenity.save()
        storage.new(amenity)
        storage.save()
        return jsonify(amenity.to_dict()), 200
    abort(400, 'Not a JSON')
