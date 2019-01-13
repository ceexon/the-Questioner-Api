from app.api.v1.views.user_views import V1_MOD, time_now
from app.api.v1.models.models import QUESTION_LIST
import datetime
from flask import Blueprint, request, jsonify, make_response


@V1_MOD.route('/questions', methods=['POST'])
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
            latest = QUESTION_LIST[-1]
            id = latest["id"]
            id = id + 1
            new_que["id"] = id
        except:
            new_que["id"] = 1

        new_que["createOn"] = time_now.strftime("%d %h %Y")
        new_que["upvotes"] = 0
        new_que["downvotes"] = 0

        QUESTION_LIST.append(new_que)
        return jsonify({"status": 201, "data": "question added successfully"}), 201

    except:
        return jsonify({"status": 204, "error": "Meetup data is required"}), 204


@V1_MOD.route("/questions/<q_id>/upvote", methods=["PATCH"])
def upvote_quiz(q_id):
    try:
        q_id = int(q_id)
    except:
        return jsonify({"status": 400, "error": "invalid question id"}), 400

    for question in QUESTION_LIST:
        if question["id"] == q_id:
            return jsonify({"status": 202, "data": "You have accepted this question"}), 202

    return jsonify({"status": 404, "error": "question not found"}), 404


@V1_MOD.route("/questions/<q_id>/downvote", methods=["PATCH"])
def downvote_quiz(q_id):
    try:
        q_id = int(q_id)
    except:
        return jsonify({"status": 400, "error": "invalid question id"}), 400

    for question in QUESTION_LIST:
        if question["id"] == q_id:
            return jsonify({"status": 200, "data": "You have rejected this question"}), 200

    return jsonify({"status": 404, "error": "question not found"}), 404
