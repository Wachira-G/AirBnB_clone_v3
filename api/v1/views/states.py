#!/usr/bin/python3
"""Handles all deflault RESTFul API actions for states."""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from werkzeug.exceptions import NotFound


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieve State objects."""
    states = storage.all('State')
    json_states = jsonify([state.to_dict() for state in states.values()])

    return json_states, 200

@app_views.route('/states/<string:id>', methods=['GET'], strict_slashes=False)
def get_a_state(id):
    """Retrieve a specific state object."""
    states = storage.all('State')
    state = [state.to_dict() for state in states.values() if state.id == id]
    if state:
        json_state = jsonify(state)
        return json_state, 200
    abort(404)


@app_views.route('/states/<string:id>', methods=['DELETE'], strict_slashes=False)
def delete_a_state(id):
    """Retrieve a specific state object."""
    states = storage.all('State')
    state = [state for state in states.values() if state.id == id]
    if state:
       storage.delete(state[0])
       storage.save()
       return {}, 200
    abort(404)


#@app_views.route('/states/', methods=['POST'], strict_slashes=False)


#@app_views.route('/states/<string:id>', methods=['PUT'], strict_slashes=False)

