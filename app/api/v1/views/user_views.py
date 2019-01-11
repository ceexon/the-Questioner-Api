from flask import Blueprint, request, jsonify
import datetime
from app.api.v1.models.models import Users
from app.api.v1.utils.validations import UserValidation

time_now = datetime.datetime.now()

v1_mod = Blueprint('apiv1', __name__)


@v1_mod.route("/signup", methods=["POST"])
def user_signup():
    try:
        user_data = request.get_json()
        validate = UserValidation(user_data)

        if not user_data:
            return jsonify({"status": 204, "error": "No data found"}), 204

        all_fields_present = validate.all_required_fields_signup()
        if not all_fields_present:
            return jsonify({"status": 400, "error": "For a successful signup ensure you input(firstName, lastName, userName, email, phone and password)"}), 400

        empty_field = validate.empty_fields_signup()
        if empty_field.lstrip() != "cannot be empty!!":
            return jsonify({"status": 422, "error": empty_field}), 422

        username_ok = validate.valid_username()
        if not username_ok:
            return jsonify({"status": 400, "error": "username can only contain a number,letter and _"}), 400

        username_available = validate.username_exists()
        if username_available:
            return jsonify({"status": 409, "error": "user with that name already exists"}), 409

        valid_email = validate.valid_email()
        if not valid_email:
            return jsonify({"status": 400, "error": "invalid email format"}), 400

        valid_password = validate.valid_password()
        if valid_password != 1:
            return jsonify({"status": 400, "error": valid_password}), 400

        new_user = validate.add_default_fields()

        Users.append(new_user)
        return jsonify({"status": 201, "data": new_user}), 201

    except:
        return jsonify({"status": 417, "error": "signup data is required"}), 417


@v1_mod.route("/login", methods=['POST'])
def user_login():
    try:
        log_data = request.get_json()
        if not log_data:
            return jsonify({"status": 204, "error": "No data found"}), 204

        try:
            if not log_data["userlog"] or not log_data["password"]:
                return jsonify({"status": 422, "error": "all fields are required(password,userlog(userName/email))"}), 422

        except:
            return jsonify({"status": 400, "error": "a key field is missing"}), 400

        actual_user = log_data["userlog"]
        using = ""
        if '@' in actual_user:
            using = "email"
        else:
            using = "userName"

        exists = False

        if using == "email":
            for user in Users:
                if user["email"] == actual_user and user["password"] == log_data["password"]:
                    exists = True
        elif using == "userName":
            for user in Users:
                if user["userName"] == actual_user and user["password"] == log_data["password"]:
                    exists = True

        if exists == True:
            return jsonify({"status": 200, "data": "logged in successfully"}), 200

        return jsonify({"status": 401, "data": "invalid login credentials"}), 401

    except:
        return jsonify({"status": 204, "error": "Login is required"})
