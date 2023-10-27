#!/usr/bin/python3
"""Index of views"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def status():
    """Return the status of the api."""
    return jsonify({"status": "OK"}), 200


@app_views.route('/stats', strict_slashes=False)
def stats():
    """retrieve number of each object by type"""
    return jsonify(storage.count())
