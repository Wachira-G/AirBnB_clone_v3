#!/usr/bin/python3
"""Handles all deflault RESTFul API actions for users."""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.user import User
from werkzeug.exceptions import NotFound


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def get_users():
    """Retrieve User objects."""
    users = storage.all("User")
    json_users = jsonify([user.to_dict() for user in users.values()])

    return json_users, 200


@app_views.route("/users/<string:id>", methods=["GET"], strict_slashes=False)
def get_a_user(id):
    """Retrieve a specific user object."""
    user = storage.get('User', id)
    if user:
        json_user = jsonify(user.to_dict())
        return json_user, 200
    abort(404)


@app_views.route(
        "/users/<string:id>",
        methods=["DELETE"],
        strict_slashes=False,
        )
def delete_a_user(id):
    """Delete a specific user object."""
    user = storage.get('User', id)
    if user:
        user.delete()
        storage.save()
        return {}, 200
    abort(404)


@app_views.route('/users/', methods=['POST'], strict_slashes=False)
def post_a_user():
    """Create a user object."""
    user_info = request.get_json()
    if user_info:
        if not user_info.get('name'):
            abort(400, 'Missing name')
        user = User(**user_info)
        storage.new(user)
        storage.save()
        return jsonify(user.to_dict()), 201
    abort(400, 'Not a JSON')


@app_views.route('/users/<string:id>', methods=['PUT'], strict_slashes=False)
def put_a_user(id):
    """Update a user object."""
    user_info = request.get_json()
    if not user_info:
        abort(404)
    user = storage.get('User', id)
    if user:
        user_dict = user.to_dict()
        user_dict.update(user_info)
        # filter out attrs
        IGNORE = ['__class__', 'id', 'created_at', 'updated_at', 'email']
        user_dict = {k: v for k, v in user_dict.items() if k not in IGNORE}
        # user = User(**user_dict)
        for key, value in user_dict.items():
            setattr(user, key, value)

        user.save()
        storage.new(user)
        storage.save()
        return jsonify(user.to_dict()), 200
    abort(400, 'Not a JSON')
