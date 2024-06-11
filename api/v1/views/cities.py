#!/usr/bin/python3
"""view for City objects"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<string:state_id>/cities', methods=['GET'])
def cities_in_state(state_id):
    """Retrieves the list of all City objects associated with a given State.

    Expects a valid state ID in the URL path and returns a JSON response containing details of all City objects belonging to that state.

    Returns:
        - A JSON response with a list of city dictionaries (200 OK).
        - A 404 Not Found error if the specified state is not found.
    """
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    city_dicts = [city.to_dict() for city in state.cities]
    return jsonify(city_dicts)


@app_views.route('/cities/<string:city_id>', methods=['GET'])
def city_by_id(city_id):
     """Retrieves a specific City object by its ID.

    Expects a city ID in the URL path and returns a JSON response with details of the matching City object.

    Returns:
        - A JSON response with the city dictionary (200 OK).
        - A 404 Not Found error if the specified city is not found.
    """
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())

@app_views.route('/cities/<string:city_id>', methods=['DELETE'])
def delete_city(city_id):
    """Deletes a City object.

    Expects a city ID in the URL path and deletes the corresponding City object from storage.

    Returns:
        - An empty JSON response (200 OK) on successful deletion.
        - A 404 Not Found error if the specified city is not found.
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return (jsonify({}))


@app_views.route('/states/<string:state_id>/cities/', methods=['POST'])
def create_city(state_id):
    """Creates a new City object associated with a given State.

    Expects a JSON request containing city data (including name) in the body and a valid state ID in the URL path.
    Validates the request content and creates a new City object with the provided information.

    Returns:
        - A JSON response with the created city dictionary (201 Created).
        - A 404 Not Found error if the specified state is not found.
        - A 400 Bad Request error if the request is not JSON or the required 'name' field is missing.
    """
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    if not request.is_json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    city_data = request.get_json()
    if 'name' not in city_data:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    city_data['state_id'] = state_id
    city = City(**city_data)
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<string:city_id>', methods=['PUT'])
def city_update(city_id):
 """Updates a City object.

    Expects a city ID in the URL path and a JSON request containing the updated city information in the body.
    Validates the request content and allows updating any attribute of the City object except for those considered read-only
    (id, state_id, created_at, updated_at).

    Returns:
        - A JSON response with the updated city dictionary (200 OK).
        - A 404 Not Found error if the specified city is not found.
        - A 400 Bad Request error if the request is not JSON.
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, attr, val)
    city.save()
    return jsonify(city.to_dict())
