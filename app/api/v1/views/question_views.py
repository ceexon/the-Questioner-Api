import datetime
from flask import Blueprint, request, jsonify, make_response
from app.api.v1.views.user_views import V1_MOD
from app.api.v1.models.models import QUESTION_LIST, MEETUP_LIST, Question, User, USER_LIST
from ..utils.validations import token_required, QuestionValidation
TIME_NOW = datetime.datetime.now()
VOTERS = []


@V1_MOD.route('/meetups/<m_id>/questions', methods=['POST'])
@token_required
def add_meetup_question(current_user, m_id):
    try:
        q_data = request.get_json()
        if not q_data:
            return jsonify({"status": 404, "error": "No data found"}), 404

        Question(MEETUP_LIST, "pass").check_id(m_id)
        a_question = Question(QUESTION_LIST, q_data)
        a_question.check_required_present(Question.required_fields)
        asker = User(USER_LIST, "user").get_current_user(current_user)
        new_question = a_question.autogen_id_and_defaults()
        new_question["meetup"] = int(m_id)
        new_question["user"] = asker["id"]
        new_question["upvotes"] = 0
        new_question["downvotes"] = 0
        new_question = a_question.save_the_data()
        return jsonify({"status": 201, "message": "question added successfully", "Question": new_question}), 201
    except TypeError:
        return jsonify({"status": 417, "error": "Question data is required"}), 417


@V1_MOD.route('/meetups/<m_id>/questions', methods=["GET"])
@token_required
def get_all_questions(current_user, m_id):
    Question(MEETUP_LIST, "pass").check_id(m_id)
    return jsonify({"Questions": QUESTION_LIST}), 200


@V1_MOD.route('/meetups/<m_id>/questions/<q_id>', methods=["GET"])
@token_required
def get_a_question_by_id(current_user, m_id, q_id):
    Question(MEETUP_LIST, "pass").check_id(m_id)
    Question(QUESTION_LIST, "pass").check_id(q_id)
    for question in QUESTION_LIST:
        if question["id"] == int(q_id):
            return jsonify({"Question": question, "status": 200}), 200


@V1_MOD.route("/meetups/<m_id>/questions/<q_id>/upvote", methods=["PATCH"])
@token_required
def upvote_quiz(current_user, m_id, q_id):
    Question(QUESTION_LIST, "pass").check_id(m_id)
    question = Question(QUESTION_LIST, "pass").check_id(q_id)
    voted = User(USER_LIST, "pass").get_current_user(current_user)
    if voted in VOTERS:
        return jsonify({"status": 403, "message": "You cannot vote more than once"}), 403
    question["upvotes"] += 1
    VOTERS.append(voted)
    return jsonify({"status": 201, "Question": question}), 201


@V1_MOD.route("/meetups/<m_id>/questions/<q_id>/downvote", methods=["PATCH"])
@token_required
def downvote_quiz(current_user, m_id, q_id):
    Question(QUESTION_LIST, "pass").check_id(m_id)
    question = Question(QUESTION_LIST, "pass").check_id(q_id)
    voted = User(USER_LIST, "pass").get_current_user(current_user)
    if voted in VOTERS:
        return jsonify({"status": 403, "message": "You cannot vote more than once"}), 403
    question["downvotes"] += 1
    VOTERS.append(voted)
    return jsonify({"status": 201, "Question": question}), 201
