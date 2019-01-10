from app.api.v1.views.user_views import v1_mod, time_now
from app.api.v1.models.models import Questions
import datetime
from flask import Blueprint, request, jsonify, make_response


@v1_mod.route('/questions', methods=['POST'])
def add_meetup_question():
    try:
        q_data = request.get_json()
        if not q_data:
            return jsonify({"status": 204, "error": "No data found"}), 204

        try:
            if not q_data["topic"] or not q_data["body"]:
                return jsonify({"status": 422, "error": "These fields are required(topic,body)"}), 422

        except:
            return jsonify({"status": 400, "error": "a key field is missing"}), 400

        new_que = {}
        for key in q_data:
            new_que[key] = q_data[key]

        try:
            latest = Questions[-1]
            id = latest["id"]
            id = id + 1
            new_que["id"] = id
        except:
            new_que["id"] = 1

        new_que["createOn"] = time_now.strftime("%d %h %Y")

        Questions.append(new_que)
        return jsonify({"status": 201, "data": "question added successfully"}), 201

    except:
        return jsonify({"status": 204, "error": "Meetup data is required"}), 204
