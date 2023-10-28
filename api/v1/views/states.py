#!/usr/bin/python3
"""Handles all deflault RESTFul API actions for states."""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State
from werkzeug.exceptions import NotFound


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_states():
    """Retrieve State objects."""
    states = storage.all("State")
    json_states = jsonify([state.to_dict() for state in states.values()])

    return json_states, 200


@app_views.route("/states/<string:id>", methods=["GET"], strict_slashes=False)
def get_a_state(id):
    """Retrieve a specific state object."""
    state = storage.get('State', id)
    if state:
        json_state = jsonify(state.to_dict())
        return json_state, 200
    abort(404)


@app_views.route(
        "/states/<string:id>",
        methods=["DELETE"],
        strict_slashes=False,
        )
def delete_a_state(id):
    """Delete a specific state object."""
    state = storage.get('State', id)
    if state:
        # delete review
        # delete place
        # delete city
        state.delete()
        storage.save()
        return {}, 200
    abort(404)


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def post_a_state():
    """Create a state object."""
    state_info = request.get_json()
    if state_info:
        if not state_info.get('name'):
            abort(400, 'Missing name')
        state = State(**state_info)
        storage.new(state)
        storage.save()
        return jsonify(state.to_dict()), 201
    abort(400, 'Not a JSON')


@app_views.route('/states/<string:id>', methods=['PUT'], strict_slashes=False)
def put_a_state(id):
    """Update a state object."""
    state_info = request.get_json()
    if not state_info:
        abort(404)
    state = storage.get('State', id)
    if state:
        state_dict = state.to_dict()
        state_dict.update(state_info)
        # filter out attrs
        IGNORE = ['__class__', 'id', 'created_at', 'update_at']
        state_dict = {k: v for k, v in state_dict.items() if k not in IGNORE}
        # state = State(**state_dict)
        for key, value in state_dict.items():
            setattr(state, key, value)

        state.save()
        storage.new(state)
        storage.save()
        return jsonify(state.to_dict()), 200
    abort(400, 'Not a JSON')
