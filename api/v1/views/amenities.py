#!/usr/bin/python3
"""Amenity objects that handles all default RESTFul API actions"""

from flask import jsonify, request, abort
from models import storage
from api.v1.views import app_views
from models.amenity import Amenity

@app_views.routes('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
  """Retrieves the list of all Amenity object"""
  amenities - storage.all(Amenity).values()
  return jsonify([amenity.to_dict() for amenity in amenities])

@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
  """Retrieves an amenity object"""
  amenity = storage.get(Amenity, amenity_id)
  if not amenity:
    abort(404)
    return jsonify(amenity.to_dict())

@app_views.route('/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
  """Deletes"""
  amenity = storage.get(Amenity, amenity_id)
  if not amenity:
    abort(404)
  storage.delete(amenity)
  storage.save()
  return jsonify({}), 200

@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
  """creates a new amenity"""
  if not request.json:
    abort(400, description="Not a JSON")
  if 'name' not in request.json:
    abort(400, description="Missing name")
  data = request.get_json()
  new_amenity = Amenity(**data)
  storage.new(new_amenity)
  storage.save()
  return jsonify(new_amenity.to_dict()), 201

@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
  amenity = storage.get(Amenity, amenity-id)
  if not amenity:
    abort(404)
  if not request.json:
    abort(400, description="Not a JSON")
  data = request.get_json()
  ignore_keys = ['id', 'created_at', 'updated_at']
  for key, value in data.items():
    if key not in ignore_keys:
      setattr(amenity, key, value)
  storage.save()
  return jsonify(amenity.to_dict()), 200
