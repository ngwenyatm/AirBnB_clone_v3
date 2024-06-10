#!/usr/bin/python3
"""State objects that handles all default RESTFul API actions"""

from models import storage
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
  """gets all states"""
  states = storage.all(State).values()
  return jsonify([state.to_dict() for state in states])

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
  """raises a 404 error"""
  state = storage.get(State, state_id)
  if not state:
    abort(404)
  return jsonify(state.to_dict())

  @app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
  def delete_state(state_id):
    """Deletes"""
    state = storage.get(State, state_id)
    if not state:
      abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200

  @app_views.route('/states', methods=['POST'], strict_slashes=False)
  def create_state():
    """Creates a state"""
    if not request.json:
      abort(400, description="Not a JSON")
    if 'name' not in request.json:
      abort(400, description="Missing name")
    data = request.get_json()
    new_state = State(**data)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201

  @app_views.route('/states/<state_id>'. methods=['PUT'], strict_slashes=False)
  def update_state(state_id):
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
