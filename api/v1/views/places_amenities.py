#!/usr/bin/python3
"""Handles all deflault RESTFul API actions for link btwn Place and Amenity."""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.amenity import Amenity
from models.place import Place
from werkzeug.exceptions import NotFound


@app_views.route(
        "/places/<string:place_id>/amenities",
        methods=["GET"],
        strict_slashes=False,
        )
def get_place_amenities(place_id):
    """Retrieve Amenity objects of a place."""
    place = storage.get('Place', place_id)
    if not place:
        abort(404)
    plc_amenities = place.amenities
    json_amenities = jsonify([
        amenity.to_dict() for amenity in plc_amenities])

    return json_amenities, 200


@app_views.route(
        "/places/<string:place_id>/amenities/<string:amenity_id>",
        methods=["DELETE"]
        )
def delete_place_amenity(place_id, amenity_id):
    """Delete an Amenity object to a Place."""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if not place:
        abort(404)
    if not amenity:
        abort(404)

    if amenity not in place.amenities:
        abort(404)

    place.amenities.remove(amenity)
    storage.save()

    return jsonify({}), 200


@app_views.route(
        "/places/<string:place_id>/amenities/<string:amenity_id>",
        methods=["POST"]
        )
def link_place_amenity(place_id, amenity_id):
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if not place:
        abort(404)
    if not amenity:
        abort(404)

    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200

    place.amenities.append(amenity)
    storage.save()

    return jsonify(amenity.to_dict()), 201
