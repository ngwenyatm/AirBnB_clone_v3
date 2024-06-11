#!/usr/bin/python3
"""
Module for handling State objects with all default RESTful API actions.

This module provides functions for retrieving, creating, updating, and deleting
State objects through Flask routes.
"""

from models import storage
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
  """
    Retrieves all State objects.

    Returns:
        JSON: A list of dictionaries representing all State objects.
    """
  states = storage.all(State).values()
  return jsonify([state.to_dict() for state in states])

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
   """
    Retrieves a specific State object.

    Args:
        state_id (str): The ID of the State object to retrieve.

    Returns:
        JSON: A dictionary representing the retrieved State object, or a 404 Not Found
            response if the State is not found.
    """
  state = storage.get(State, state_id)
  if not state:
    abort(404)
  return jsonify(state.to_dict())

  @app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
  def delete_state(state_id):
     """
    Deletes a specific State object.

    Args:
        state_id (str): The ID of the State object to delete.

    Returns:
        JSON: An empty JSON object with a 200 OK status code if the State is deleted
            successfully, or a 404 Not Found response if the State is not found.
    """
    state = storage.get(State, state_id)
    if not state:
      abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200

  @app_views.route('/states', methods=['POST'], strict_slashes=False)
  def create_state():
    """
    Creates a new State object.

    Returns:
        JSON: A dictionary representing the newly created State object, or a 400 Bad Request
            response if the request is invalid (e.g., missing required fields, invalid JSON format).
    """
    if not request.json:
      abort(400, description="Not a JSON")
    if 'name' not in request.json:
      abort(400, description="Missing name")
    data = request.get_json()
    new_state = State(**data)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201

  @app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
  def update_state(state_id):
    """
    Updates a specific State object.

    Args:
        state_id (str): The ID of the State object to update.

    Returns:
        JSON: A dictionary representing the updated State object, or a 400 Bad Request
            response if the request is invalid (e.g., not a JSON request), or a 404 Not Found
            response if the State is not found.
    """
      state = storage.get(State, state_id)
      if not state:
          abort(404)
      if not request.json:
          abort(400, description="Not a JSON")
      data = request.get_json()
      ignore_keys = ['id', 'created_at', 'updated_at']
      for key, value in data.items():
          if key not in ignore_keys:
              setattr(state, key, value)
      storage.save()
      return jsonify(state.to_dict()), 200
