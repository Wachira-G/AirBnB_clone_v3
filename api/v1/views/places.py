#!/usr/bin/python3
"""Handles all deflault RESTFul API actions for places."""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.place import Place
from werkzeug.exceptions import NotFound


@app_views.route(
        "/cities/<string:city_id>/places",
        methods=["GET"],
        strict_slashes=False
        )
def get_places(city_id):
    """Retrieve Place objects."""
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    places = storage.all("Place")
    json_places = jsonify(
            [place.to_dict() for place in places.values()
                if place.city_id == city_id])

    return json_places, 200


@app_views.route("/places/<string:id>", methods=["GET"], strict_slashes=False)
def get_a_place(id):
    """Retrieve a specific place object."""
    place = storage.get('Place', id)
    if place is None:
        abort(404)
    if place:
        json_place = jsonify(place.to_dict())
        return json_place, 200


@app_views.route(
        "/places/<string:id>",
        methods=["DELETE"],
        strict_slashes=False,
        )
def delete_a_place(id):
    """Delete a specific place object."""
    place = storage.get('Place', id)
    if place is None:
        abort(404)
    if place:
        place.delete()
        storage.save()
        return {}, 200


@app_views.route(
        '/cities/<string:city_id>/places/',
        methods=['POST'], strict_slashes=False
        )
def post_a_place(city_id):
    """Create a place object."""
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    place_info = request.get_json()
    if place_info is None:
        abort(400, 'Not a JSON')
    if place_info:
        if not place_info.get('user_id'):
            abort(400, 'Missing user_id')
        user = storage.get('User', place_info['user_id'])
        if user is None:
            abort(404)
        if not place_info.get('name'):
            abort(400, 'Missing name')
        place_info.update({"city_id": city_id})
        place = Place(**place_info)
        storage.new(place)
        storage.save()
        return jsonify(place.to_dict()), 201


@app_views.route('/places/<string:id>', methods=['PUT'], strict_slashes=False)
def put_a_place(id):
    """Update a place object."""
    place = storage.get('Place', id)
    if place is None:
        abort(404)
    place_info = request.get_json()
    if place_info is None:
        abort(400, 'Not a JSON')
    if place:
        place_dict = place.to_dict()
        place_dict.update(place_info)
        # filter out attrs
        IGNORE = [
                '__class__', 'id', 'created_at',
                'updated_at', 'user_id', 'city_id',
                ]
        place_dict = {k: v for k, v in place_dict.items() if k not in IGNORE}
        # place = Place(**place_dict)
        for key, value in place_dict.items():
            setattr(place, key, value)

        place.save()
        storage.new(place)
        storage.save()
        return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_places():
    """Retrieves all Place objects depending on JSON in body of the request."""
    info = request.get_json()

    if info is None:
        abort(400, 'Not a JSON')

    amenities = set(info.get('amenities', []))
    states = set(info.get('states', []))
    cities = set(info.get('cities', []))

    all_places = storage.all("Place").values()

    if not info or (not states and not cities and not amenities):
        return jsonify([place.to_dict() for place in all_places]), 200

    places = set()

    for state_id in states:
        state_cities = storage.all("City").values()
        state_cites = [city.id for city in state_cities if city.id == state_id]
        for city_id in state_cities:
            for place in all_places:
                if place.city_id == city_id:
                    places.add(place)
    for city_id in cities:
        for place in all_places:
            if place.city_id == city_id:
                places.add(place)

    # filter amenities
    filtered_places = []
    for place in places:
        if storage == 'db':
            place_amenities = {amenity.id for amenity in place.amenities}
            if amenities.issubset(place_amenities):
                filtered_places.append(place.to_dict())
    return jsonify(filtered_places), 200
