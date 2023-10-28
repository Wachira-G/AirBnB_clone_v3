#!/usr/bin/python3
"""Handles all deflault RESTFul API actions for places."""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.place import Place
from werkzeug.exceptions import NotFound


@app_views.route("/places", methods=["GET"], strict_slashes=False)
def get_places():
    """Retrieve Place objects."""
    places = storage.all("Place")
    json_places = jsonify([place.to_dict() for place in places.values()])

    return json_places, 200


@app_views.route("/places/<string:id>", methods=["GET"], strict_slashes=False)
def get_a_place(id):
    """Retrieve a specific place object."""
    place = storage.get('Place', id)
    if place:
        json_place = jsonify(place.to_dict())
        return json_place, 200
    abort(404)


@app_views.route(
        "/places/<string:id>",
        methods=["DELETE"],
        strict_slashes=False,
        )
def delete_a_place(id):
    """Delete a specific place object."""
    place = storage.get('Place', id)
    if place:
        place.delete()
        storage.save()
        return {}, 200
    abort(404)


@app_views.route('/places/', methods=['POST'], strict_slashes=False)
def post_a_place():
    """Create a place object."""
    place_info = request.get_json()
    if place_info:
        if not place_info.get('name'):
            abort(400, 'Missing name')
        place = Place(**place_info)
        storage.new(place)
        storage.save()
        return jsonify(place.to_dict()), 201
    abort(400, 'Not a JSON')


@app_views.route('/places/<string:id>', methods=['PUT'], strict_slashes=False)
def put_a_place(id):
    """Update a place object."""
    place_info = request.get_json()
    if not place_info:
        abort(404)
    place = storage.get('Place', id)
    if place:
        place_dict = place.to_dict()
        place_dict.update(place_info)
        # filter out attrs
        IGNORE = ['__class__', 'id', 'created_at', 'update_at']
        place_dict = {k: v for k, v in place_dict.items() if k not in IGNORE}
        # place = Place(**place_dict)
        for key, value in place_dict.items():
            setattr(place, key, value)

        place.save()
        storage.new(place)
        storage.save()
        return jsonify(place.to_dict()), 200
    abort(400, 'Not a JSON')
