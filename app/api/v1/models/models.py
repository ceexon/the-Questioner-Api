""" Contains all data for users models and questions"""

import datetime
import uuid
from werkzeug.security import generate_password_hash
from flask import jsonify, abort, make_response
TIME_NOW = datetime.datetime.now()

USER_LIST = []
MEETUP_LIST = []
QUESTION_LIST = []


class BaseModels:
    """"This performs all basic actions performed on all data sets"""

    def __init__(self, data_model, view_data):
        """" initialising parameters to be passed in the BaseModels object """
        self.d_b = data_model
        self.data = view_data

    def autogen_id_and_defaults(self):
        """ Autogenerate an id and add default fields to the data """
        if not self.d_b:
            self.data["id"] = 1
        else:
            new_id = self.d_b[-1]["id"] + 1
            self.data["id"] = new_id

        self.data["createOn"] = TIME_NOW.strftime("%D")
        hashed_password = generate_password_hash(
            self.data['password'], method="sha256")
        self.data["password"] = hashed_password
        self.data['public_id'] = str(uuid.uuid4())
        return self.data

    def check_required_present(self, required_fields):
        """ checks if data has all required fields and their values """
        error = ""
        for field in required_fields:
            try:
                test_presence = self.data[field]
                if not test_presence or not test_presence.strip():
                    if not test_presence:
                        error = field + " cannot be empty!!"
                    elif not test_presence.strip():
                        error = field + " cannot contain whitespace only"
                    abort(make_response(
                        jsonify({"status": 422, "error": error}), 422))
            except KeyError:
                error = field + " field is missing"
                abort(make_response(
                    jsonify({"status": 400, "error": error}), 400))
        return 1

    def save_the_data(self):
        """ appends new data to the appropriate data model """
        self.d_b.append(self.data)
        return self.data

    def delete_the_data(self):
        """ delete selected data from the appropriate db """
        self.d_b.remove(self.data)
        return jsonify({"status": 200, "data": "user has been deleted"}), 200

    def check_exists(self, field_to_check, the_value):
        """ checks existence of of given data in the given data model """
        exists = 0
        if self.d_b:
            available = [
                value for value in self.d_b if value[field_to_check] == the_value]
            if available:
                exists = 1
        return exists


class UserModels(BaseModels):
    """ Model for user data """

    required_signup = ["firstName", "lastName",
                       "userName", "email", "phone", "password"]
    required_login = ["userlog", "password"]

    def add_admin_status(self):
        """ sets only the first user as admin """
        self.data["isAdmin"] = False
        if not self.d_b:
            self.data["isAdmin"] = True

        return self.data
