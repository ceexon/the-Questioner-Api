""" Validation for data received from a user """

import os
import re
from functools import wraps
import jwt
from werkzeug.security import check_password_hash
from flask import abort, make_response, jsonify, request
from ..models.models import USER_LIST, UserModels

EMAIL_REGEX = re.compile(r'(\w+[.|\w])*@(\w+[.])*\w+')
PASSWORD_RE = re.compile('^(?=.*[!$?])(?=.*[a-z])(?=.*[A-Z]).{8}$')


class UserValidation():
    """ THis class validates all user data input from a user for signup and login """

    correct_details = []

    def __init__(self, user_data):
        """ set parameter to be passed whet calling the object """
        self.data = user_data

    def valid_username(self):
        """ validates the username parsed """
        if re.search("[!@#$%^&*-/\\')(;\"`<>?:|}{~ ]", self.data["userName"]):
            abort(make_response(
                jsonify({"status": 400, "error": "username can only be a letter or _"}), 400))

    def valid_email(self):
        """ validates the email parsed """
        if not EMAIL_REGEX.match(self.data["email"]):
            abort(make_response(
                jsonify({"status": 400, "error": "invalid email format!!"}), 400))

    def valid_password(self):
        """ validates the password parsed """
        symbols = '$!#$@*'
        pwd = self.data["password"]
        if (len(pwd) >= 6 and
                any(c.isdigit() for c in pwd) and
                any(c.isupper() for c in pwd) and
                any(c in symbols for c in pwd) and
                all(c.isalnum() or c in symbols for c in pwd)):
            pass
        else:
            abort(make_response(jsonify(
                {"status": 400, "error": "password should have number, upper and lower letters + a special character"}), 400))

    def check_signup_exists(self):
        """ check if user signing up exists """
        in_users = UserModels(USER_LIST, self.data)
        if in_users.check_exists("userName", self.data["userName"]):
            abort(make_response(jsonify(
                {"status": 409, "error": "user with the username already exists"}), 409))
        if in_users.check_exists("email", self.data["email"]):
            abort(make_response(
                jsonify({"status": 409, "error": "user with that email already exists"}), 409))

    def confirm_login(self, login_choice):
        if "@" in login_choice:
            login_choice = "email"
        else:
            login_choice = "userName"

        self.correct_details = [user for user in USER_LIST if self.data["userlog"]
                                == user[login_choice] and check_password_hash(user["password"], self.data['password'])]
        if self.correct_details == []:
            error = "invalid " + login_choice + " or pasword!!"
            abort(make_response(
                jsonify({"status": 401, "error": error}), 401))


def token_required(func_tion):
    """ to check authentication token"""
    @wraps(func_tion)
    def decorated(*args, **kwargs):
        token = None

        if "x-access-token" in request.headers:
            token = request.headers['x-access-token']

        if not token:
            abort(make_response(jsonify({"message": "Token is missing"}), 401))

        try:
            data = jwt.decode(token, os.getenv("SECRET_KEY"))
            current_user = data["userName"]

        except ValueError:
            return jsonify({"message": "Token is invalid or expired"}), 401

        return func_tion(current_user, *args, **kwargs)
    return decorated
