from app.api.v1.views.user_views import v1_mod, time_now
from app.api.v1.models.models import Meetups
import datetime
from flask import Blueprint, request, jsonify, make_response


@v1_mod.route('/meetups', methods=['POST'])
def create_meetup():
    try:
        meet_data = request.get_json()
        if not meet_data:
            return jsonify({"status": 204, "error": "No data found"}), 204

        try:
            if not meet_data["topic"] or not meet_data["location"] or not meet_data["happenOn"]:
                return jsonify({"status": 422, "error": "These fields are required(topic,location,happenOn)"}), 422

        except:
            return jsonify({"status": 400, "error": "a key field is missing"}), 400

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
        return jsonify({"status": 204, "error": "Meetup data is required"}), 204


@v1_mod.route('/meetups', methods=['GET'])
def view_meetup():
    if Meetups == []:
        return jsonify({"status": 404, "error": "no meetups found"}), 404

    return jsonify({"status": 200, "data": Meetups}), 200
