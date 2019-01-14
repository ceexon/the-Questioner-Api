""" contains all endpoints for user functions such as signup and login """

import os
import datetime
import jwt
from flask import Blueprint, request, jsonify
from app.api.v1.models.models import USER_LIST, UserModels
from app.api.v1.utils.validations import UserValidation
V1_MOD = Blueprint('apiv1', __name__)
KEY = os.getenv("SECRET")


@V1_MOD.route("/signup", methods=["POST"])
def user_signup():
    """ endpoint for user to create account """
    try:
        user_data = request.get_json()
        if not user_data:
            return jsonify({"status": 404, "error": "no userdata data!!"}), 404
        validate = UserValidation(user_data)
        users = UserModels(USER_LIST, user_data)
        users.check_required_present(users.required_signup)
        validate.valid_username()
        validate.valid_email()
        validate.valid_password()
        validate.check_signup_exists()
        new_user = users.autogen_id_and_defaults()
        users.add_admin_status()
        new_user = users.save_the_data()
        return jsonify({"status": 201, "data": new_user}), 201
    except TypeError:
        return jsonify({"status": 417, "error": "Expecting signup data!!"}), 417


@V1_MOD.route("/users", methods=["GET"])
def all_users():
    """ Endpoint to return all users present """
    return jsonify(USER_LIST)


@V1_MOD.route("/login", methods=['POST'])
def user_login():
    """ endpoint for users to sign in """
    try:
        log_data = request.get_json()
        if not log_data:
            return jsonify({"status": 404, "error": "No data found"}), 404

        users = UserModels(USER_LIST, log_data)
        validate = UserValidation(log_data)
        users.check_required_present(users.required_login)
        validate.confirm_login(log_data["userlog"])
        logged_in_user = validate.correct_details[0]
        exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        token = jwt.encode(
            {"userName": logged_in_user['userName'], 'exp': exp}, KEY,
            algorithm='HS256')
        return jsonify({"status": 200, "message": "logged in successfully",
                        "token": token.decode("utf-8", KEY)}), 200
    except TypeError:
        return jsonify({"status": 417, "error": "Expecting Login data!!"}), 417
