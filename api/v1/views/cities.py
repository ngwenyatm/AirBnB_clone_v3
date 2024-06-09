#!/usr/bin/python3
"""view for City objects"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<string:state_id>/cities', methods=['GET'])
def cities_in_state(state_id):
    """Retrieves the list of all City objects of a State"""
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    city_dicts = [city.to_dict() for city in state.cities]
    return jsonify(city_dicts)


@app_views.route('/cities/<string:city_id>', methods=['GET'])
def city_by_id(city_id):
    """Retrieves a City object"""
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())

@app_views.route('/cities/<string:city_id>', methods=['DELETE'])
def delete_city(city_id):
    """Deletes a City object"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return (jsonify({}))


@app_views.route('/states/<string:state_id>/cities/', methods=['POST'])
def create_city(state_id):
    """Creates a City"""
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
    """Updates a City object"""
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
