#!/usr/bin/python3
"""Handles all deflault RESTFul API actions for cities."""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.city import City
from werkzeug.exceptions import NotFound


@app_views.route(
        "/states/<state_id>/cities", methods=["GET"], strict_slashes=False)
def get_cities(state_id):
    """Retrieve City objects."""
    state = storage.get('State', state_id)
    if not state:
        abort(404)
    cities = storage.all("City")
    json_cities = jsonify(
        [city.to_dict() for city in cities.values()
         if city.state_id == state_id])

    return json_cities, 200


@app_views.route("/cities/<string:id>", methods=["GET"], strict_slashes=False)
def get_a_city(id):
    """Retrieve a specific city object."""
    city = storage.get('City', id)
    if city:
        json_city = jsonify(city.to_dict())
        return json_city, 200
    abort(404)


@app_views.route(
        "/cities/<string:id>",
        methods=["DELETE"],
        strict_slashes=False,
        )
def delete_a_city(id):
    """Delete a specific city object."""
    city = storage.get('City', id)
    if city:
        city.delete()
        storage.save()
        return {}, 200
    abort(404)


@app_views.route(
        '/states/<state_id>/cities/', methods=['POST'], strict_slashes=False)
def post_a_city(state_id):
    """Create a city object."""
    state = storage.get('State', state_id)
    if not state:
        abort(404)

    city_info = request.get_json()
    if city_info:
        if not city_info.get('name'):
            abort(400, 'Missing name')
        city_info.update({"state_id": state_id})
        city = City(**city_info)
        storage.new(city)
        storage.save()
        return jsonify(city.to_dict()), 201
    abort(400, 'Not a JSON')


@app_views.route('/cities/<string:id>', methods=['PUT'], strict_slashes=False)
def put_a_city(id):
    """Update a city object."""
    city_info = request.get_json()
    if not city_info:
        abort(404)
    city = storage.get('City', id)
    if city:
        city_dict = city.to_dict()
        city_dict.update(city_info)
        # filter out attrs
        IGNORE = ['__class__', 'id', 'created_at', 'updated_at', 'state_id']
        city_dict = {k: v for k, v in city_dict.items() if k not in IGNORE}
        # city = City(**city_dict)
        for key, value in city_dict.items():
            setattr(city, key, value)

        city.save()
        storage.new(city)
        storage.save()
        return jsonify(city.to_dict()), 200
    abort(400, 'Not a JSON')
