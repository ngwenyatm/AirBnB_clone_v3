#!/usr/bin/python3
"""
View for Reviews that handles all RESTful API actions
"""

from flask import jsonify, request, abort
from models import storage
from models.review import Review
from api.v1.views import app_views


@app_views.route('/places/<target_place_id>/reviews', methods=['GET'])
def retrieve_all_reviews_for_place(target_place_id, user_id=None):
    """ Retrieves the list of all Review objects of a Place """
    place = storage.get("Place", target_place_id)
    if place is None:
        abort(404, "Place not found")
    place_reviews = [review.to_json() for review in storage.all("Review").values()
        if review.place_id == target_place_id]
    if user_id:
        place_reviews = [review for review in place_reviews if review['user_id'] == user_id]
    return jsonify(place_reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def retrieve_review(review_id):
    """ Retrieves a Review object. """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404, "Review not found")
    return jsonify(review.to_json())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """ Deletes a Review object """
    empty_dict = {}
    review = storage.get("Review", review_id)
    if review is None:
        abort(404, "Review not found")
    storage.delete(review)
    storage.save()
    return jsonify(empty_dict), 200


@app_views.route('/places/<target_place_id>/reviews', methods=['POST'])
def create_review(target_place_id):
    """ Creates a Review """
    place = storage.get("Place", target_place_id)
    if not place:
        abort(404, "Place not found")
    review_data = request.get_json()
    if not review_data:
        abort(400, "Not a JSON request")
    required_fields = ["user_id", "text"]
    missing_fields = [field for field in required_fields if field not in review_data]
    if missing_fields:
        abort(400, "Missing required fields: {}".format(', '.join(missing_fields)))
    user = storage.get("User", review_data["user_id"])
    if not user:
        abort(404, "User not found")
    new_review = Review(**review_data)
    new_review.place_id = target_place_id
    new_review.save()
    return jsonify(new_review.to_json()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """ Updates a Review object"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404, "Review not found")
    review_data = request.get_json()
    if review_data is None:
        abort(400, "Not a JSON request")
    for key, value in review_data.items():
        ignore_keys = ["id", "user_id", "place_id", "created_at", "updated_at"]
        if key not in ignore_keys:
            review.bm_update(key, value)
    review.save()
    return jsonify(review.to_json()), 200
