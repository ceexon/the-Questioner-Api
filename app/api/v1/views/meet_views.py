from app.api.v1.views.user_views import v1_mod, time_now
from app.api.v1.models.models import Meetups
from app.api.v1.utils.validations import token_required
import datetime
from flask import Blueprint, request, jsonify, make_response, abort

@v1_mod.route('/meetups', methods=['POST'])
def create_meetup():
    try:
        meet_data = request.get_json()
        if not meet_data:
            abort(make_response(jsonify({"status": 400, "error": "No data found"}), 400))

        try:
            if not meet_data["topic"] or not meet_data["location"] or not meet_data["happenOn"]:
                abort(make_response(jsonify({"status": 422, "error": "These fields are required(topic,location,happenOn)"}), 422))

        except:
            abort(make_response(jsonify({"status": 400, "error": "a key field is missing"}), 400))

        new_meet = {}
        for key in meet_data:
            new_meet[key] = meet_data[key]

        try:
            latest = Meetups[-1]
            id = latest["id"]
            id = id + 1
            new_meet["id"] = id
        except:
            new_meet["id"] = 1

        new_meet["createOn"] = time_now.strftime("%d %h %Y")

        Meetups.append(new_meet)
        return jsonify({"status": 201, "data": new_meet}), 201

    except:
        abort(make_response(jsonify({"status": 404, "error": "Meetup data is required"}), 404))


@v1_mod.route('/meetups', methods=['GET'])
def view_meetup():
    if Meetups == []:
        abort(make_response(jsonify({"status": 404, "error": "no meetups found"}), 404))

    return jsonify({"status": 200, "data": Meetups}), 200


@v1_mod.route('/meetups/upcoming', methods=['GET'])
def view_upcoming_meetup():
    if Meetups == []:
        abort(make_response(jsonify({"status": 404, "error": "no meetups found"}), 404))

    return jsonify({"status": 200, "data": Meetups}), 200


@v1_mod.route('/meetups/<m_id>', methods=['GET'])
def view_single_meetup(m_id):
    if Meetups == []:
        abort(make_response(jsonify({"status": 404, "error": "no meetups found"}), 404))

    try:
        m_id = int(m_id)
    except:
        abort(make_response(jsonify({"status": 400, "error": "invalid meet id,use int"}), 400))

    for meet in Meetups:
        if meet["id"] == m_id:
            return jsonify({"status": 200, "data": meet})

    abort(make_response(jsonify({"status": 404, "data": "meetup not found"}), 404))


@v1_mod.route('/meetups/<m_id>', methods=['DELETE'])
def delete_meetup(m_id):
    if Meetups == []:
        abort(make_response(jsonify({"status": 404, "error": "no meetups found"}), 404))

    try:
        m_id = int(m_id)
    except:
        abort(make_response(jsonify({"status": 400, "error": "invalid meet id,use int"}), 400))

    for meet in Meetups:
        if meet["id"] == m_id:
            Meetups.remove(meet)
            return jsonify({"status": 200, "data": "meetup deleted successfully"}), 200

    abort(make_response(jsonify({"status": 404, "data": "meetup not found"}), 404))
