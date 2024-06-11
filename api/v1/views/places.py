#!/usr/bin/python3
"""
Flask application blueprint for managing places within a city.

This blueprint defines API endpoints for retrieving, creating, updating, and deleting
place objects associated with a specific city.
"""

from flask import abort,jsonify, request
from models.city import City
from models.place import Place
from models.user import User
from api.v1.views import app_views
from models import storage

app_views.route('/cities/<city_id>/places', methods=['GET'])
def retrieve_places_in_city(target_city_id):
 """
  Retrieves all places associated with a specified city identified by its ID.

  This endpoint fetches all place objects linked to the city with the provided
  `target_city_id` and returns them as a JSON-formatted list.

  Args:
      target_city_id (str): The ID of the city to retrieve places for.

  Returns:
      JSON: A JSON-formatted list containing information about the retrieved places.
          An empty list will be returned if no places are found.

  Raises:
      HTTPException: A 404 Not Found exception if the city with the provided ID
                     cannot be found.
  """
  target_city = storage.get(City, target_city_id)
  if not target_city:
    return abort(404)
  city_places = [place.to_dict() for place in target_city.places]
  return jsonify(city_places)

app_views.route('/places/<place_id>', methods=['GET'])
def retrieve_place(target_place_id):
   """
    Retrieves a single place object identified by its ID.

    This endpoint fetches the place object with the provided `target_place_id` and
    returns it as a JSON-formatted response.

    Args:
        target_place_id (str): The ID of the place to retrieve.

    Returns:
        JSON: A JSON-formatted representation of the retrieved place,
              or a 404 Not Found response if the place cannot be found.
    """
    place = storage.get("Place", target_place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_json())

@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(target_place_id=None):
   """
  Deletes a place object identified by its ID.

  This endpoint removes the place object with the provided `target_place_id` from
  the storage system.

  Args:
      target_place_id (str): The ID of the place to delete.

  Returns:
      JSON: An empty JSON object with a 200 OK status code upon successful
             deletion, or a 404 Not Found response if the place cannot be found.
  """
  place_to_delete = storage.get("Place", target_place_id)
  if place_to_delete is None:
      abort(404)
  storage.delete(place_to_delete)
  return jsonify({}), 200

@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(target_city_id):
  """
  Creates a new place object associated with a city identified by its ID.

  This endpoint expects a JSON-formatted request body containing details for the
  new place. It then creates a new `Place` object, links it to the specified city,
  and persists it to storage.

  Args:
      target_city_id (str): The ID of the city to associate the new place with.

  Returns:
      JSON: A JSON-formatted representation of the newly created place object
             with a 201 Created status code.

  Raises:
      HTTPException: A 404 Not Found exception if the city with the provided ID
      """
  target_city = storage.get(City, target_city_id)
  if not target_city:
    return abort(404, "City not found")
  request_data = request.get_json()
  if not request_data:
    abort(400, "Not a JSON request")
  if "user_id" not in request_data:
    abort(400, "Missing user_id field")
  if "name" not in request_data:
    abort(400, "Missing name field")
  associated_user = storage.get(User, request_data["user_id"])
  if not associated_user:
    return abort(404, "User not found")

  request_data["city_id"] = target_city_id
  new_place = Place(**request_data)
  new_place.save()
  return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
"""
Updates a specific place object.

This view function handles PUT requests to the endpoint `/places/<place_id>`.

Args:
    place_id (str): The ID of the place to update.

Returns:
    JSON: A dictionary representing the updated place, or a 400 Bad Request response
         if the request is invalid (e.g., not a valid JSON request), or a 404 Not Found
         response if the place is not found.

Raises:
    HTTPException: If the request is not a valid PUT request.
"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    request_data = request.get_json()
    if request_data is None:
        abort(400, "Not a JSON")
    for field, value in request_data.items():
        ignored_fields = ["id", "user_id", "city_id", "created_at", "updated_at"]
        if field not in ignored_fields:
            place.update_attribute(field, value)
    place.save()
    place_json = place.to_json()
    return jsonify(place_json), 200

