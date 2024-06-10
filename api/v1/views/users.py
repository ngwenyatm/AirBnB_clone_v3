#!/usr/bin/python3
"""User object that handles all default RESTFul API actions"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.user import User

@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
  """Retrieves all user objects"""
  users = storage.all(User).values()
  return jsonify([user.to_dict() for user in users])


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
  """Deletes an object"""
  user = storage.get(User, user_id)
  if user is None:
    abort(404)
  storage.delete(user)
  storage.save()
  return jsonify({}), 200

@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
  """creates a user""
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
