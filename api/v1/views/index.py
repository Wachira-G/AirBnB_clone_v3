#!/usr/bin/python3
"""Index of views"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """Return the status of the api."""
    return jsonify({"status": "OK"}), 200


@app_views.route('/stats', strict_slashes=False)
def stats():
    """retrieve number of each object by type"""
    values = {}
    counts = {
            "Amenity": "amenities",
            "City": "cities",
            "Place": "places",
            "Review": "reviews",
            "State": "states",
            "User": "users"
            }
    for key, value in counts.items():
        values[value] = storage.count(key)
    return jsonify(values)
