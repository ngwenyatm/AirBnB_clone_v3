ces that handles all RESTful API actions
"""

from flask import abort,jsonify, request
from models.city import City
from models.place import Place
from models.user import User
from api.v1.views import app_views
from models import storage

app_views.route('/cities/<city_id>/places', methods=['GET'])
def retrieve_places_in_city(target_city_id):
  """ Retrieves all places associated with a specific city """
  target_city = storage.get(City, target_city_id)
  if not target_city:
    return abort(404)
  city_places = [place.to_dict() for place in target_city.places]
  return jsonify(city_places)

app_views.route('/places/<place_id>' methods=['GET'])
def retrieve_place(target_place_id):
    """ Retrieves a Place object """
    place = storage.get("Place", target_place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_json())

@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(target_place_id=None):
  """ Deletes a Place object """
  place_to_delete = storage.get("Place", target_place_id)
  if place_to_delete is None:
      abort(404)
  storage.delete(place_to_delete)
  return jsonify({}), 200

@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(target_city_id):
  """
  Creates a new Place object associated with a City.
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
    """ Updates a Place object """
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

