#!/usr/bin/python3
"""
User object that handles all default RESTFul API actions.

This module provides functions for retrieving, creating, and deleting User objects.
"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.user import User

@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """
    Retrieves all User objects.

    Returns:
        JSON: A list of dictionaries representing all User objects.
    """
  users = storage.all(User).values()
  return jsonify([user.to_dict() for user in users])


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """
    Deletes a specific User object.

    Args:
        user_id (str): The ID of the User object to delete.

    Returns:
        JSON: An empty JSON object with a 200 OK status code if the User is deleted
            successfully, or a 404 Not Found response if the User is not found.
    """
  user = storage.get(User, user_id)
  if user is None:
    abort(404)
  storage.delete(user)
  storage.save()
  return jsonify({}), 200

@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """
    Creates a new User object.

    Returns:
        JSON: A dictionary representing the newly created User object, or a 400 Bad Request
            response if the request is invalid (e.g., missing required fields, invalid JSON format).
    """
  if not request.json:
    abort(400, "Not a JSON")
  if 'email' not in request.json:
    abort(400, "Missing email")
  if 'password' not in request.json:
    abort(400, "Missing password")
  data = request.get_json()
  user = User(**data)
  storage.new(user)
  storage.save()
  return jsonify(user.to_dict()), 201
