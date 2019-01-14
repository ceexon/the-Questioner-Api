""" api endpoints for working with meetups """

from flask import request, jsonify, make_response, abort
from app.api.v1.views.user_views import V1_MOD
from app.api.v1.models.models import MEETUP_LIST, MeetUpModels, USER_LIST, UserModels
from app.api.v1.utils.validations import token_required


@V1_MOD.route('/meetups', methods=['POST'])
@token_required
def create_meetup(current_user):
    """ endpoint to create new meetups """
    try:
        meet_data = request.get_json()
        if not meet_data:
            abort(make_response(
                jsonify({"status": 400, "error": "No meetup data found"}), 400))
        user = UserModels(USER_LIST, "user").get_current_user(current_user)
        if not user["isAdmin"]:
            return jsonify({"status": 403, "error": "you cannot create a meetup"}), 403
        meets = MeetUpModels(MEETUP_LIST, meet_data)
        meets.check_required_present(meets.meetup_required)
        meets.prevent_metups_duplicates()
        meets.check_tags()
        new_meet = meets.autogen_id_and_defaults()
        new_meet = meets.save_the_data()
        return jsonify({"status": 201, "data": new_meet}), 201

    except TypeError:
        abort(make_response(
            jsonify({"status": 404, "error": "Meetup data is required"}), 404))


@V1_MOD.route('/meetups', methods=['GET'])
def view_meetup():
    """ endpoint to view all existing meetups """
    meets_all = MeetUpModels(MEETUP_LIST, "pass")
    all_meets = meets_all.show_all_meetups()
    return jsonify({"status": 200, "data": all_meets}), 200


@V1_MOD.route('/meetups/upcoming', methods=['GET'])
def view_upcoming_meetup():
    """ endpoint to view all upcoming meetups """
    if MEETUP_LIST == []:
        abort(make_response(
            jsonify({"status": 404, "error": "no meetups found"}), 404))

    return jsonify({"status": 200, "data": MEETUP_LIST}), 200


@V1_MOD.route('/meetups/<m_id>', methods=['GET'])
@token_required
def view_single_meetup(current_user, m_id):
    """ endpoint to view a single meetup by id_int """
    the_id = MeetUpModels(MEETUP_LIST, "pass").check_id(m_id)
    user = UserModels(USER_LIST, "user").get_current_user(current_user)
    if not user:
        return jsonify({"status": 403, "error": "please login to access this meetup"}), 403
    if the_id in MEETUP_LIST:
        return jsonify({"status": 200, "data": the_id}), 200
    return jsonify({"status": 404, "data": "meetup not found"}), 404


@V1_MOD.route('/meetups/<m_id>', methods=['DELETE'])
@token_required
def delete_meetup(current_user, m_id):
    """ endpoint to delete meetups by id """
    to_delete = MeetUpModels(MEETUP_LIST, "pass").check_id(m_id)
    user = UserModels(USER_LIST, "user").get_current_user(current_user)
    if not user["isAdmin"]:
        return jsonify({"status": 403, "error": "you cannot create a meetup"}), 403
    MEETUP_LIST.remove(to_delete)
    return jsonify({"status": 200, "data": "meetup delete successful"}), 200
