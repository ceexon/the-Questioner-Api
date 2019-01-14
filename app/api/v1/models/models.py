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
                    elif not str(test_presence).strip():
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

    def delete_the_data(self, an_id):
        """ delete selected data from the appropriate db """
        for value in self.d_b:
            if value["id"] == an_id:
                self.d_b.pop(an_id)
                return jsonify({"status": 200, "data": "deleted successfully"}), 200
        abort(make_response(
            jsonify({"status": 404, "error": "meetup not found"}), 404))

    def check_exists(self, field_to_check, the_value):
        """ checks existence of of given data in the given data model """
        exists = 0
        if self.d_b:
            available = [
                value for value in self.d_b if value[field_to_check] == the_value]
            if available:
                exists = 1
        return exists

    def check_id(self, the_id):
        """ conver string id from url to int and tries to find it in the data set """
        for data in self.d_b:
            try:
                if data["id"]:
                    try:
                        if data["id"] == int(the_id):
                            return data
                    except ValueError:
                        abort(make_response(jsonify(
                            {"status": 400,
                             "error": "the id you parsed in invalid, can only be a number"}), 400))
            except KeyError:
                pass
        abort(make_response(
            jsonify({"status": 404,
                     "error": "requested id was not found or is out of range"}), 404))


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

        self.data['public_id'] = str(uuid.uuid4())
        hashed_password = generate_password_hash(
            self.data['password'], method="sha256")
        self.data["password"] = hashed_password
        return self.data

    def get_current_user(self, p_id):
        """ gets a user by their public_id """
        for user in self.d_b:
            if user["userName"] == p_id:
                return user
        abort(make_response(
            jsonify({"status": 404, "error": "user not found try logging in again"})))


class MeetUpModels(BaseModels):
    """ stores data for meetups """
    meetup_required = ["location", "happenOn", "topic"]

    def check_tags(self):
        """ checks if data has all required fields and their values """
        try:
            tags = self.data["tags"]
            if not tags:
                abort(make_response(
                    jsonify({"status": 422,
                             "error": "at least 1 tag is required[#name_of_tag]"}), 422))
            for tag in tags:
                if not str(tag).strip():
                    abort(make_response(jsonify(
                        {"status": 422, "error": "tag input cannot be empty whitespace!!"}), 422))
        except KeyError:
            abort(make_response(
                jsonify({"status": 400, "error": "tag field is missing"}), 400))

    def prevent_metups_duplicates(self):
        """" prevent duplication of meetups """
        for meet in self.d_b:
            if meet["location"] == self.data["location"] and meet["happenOn"] == self.data["happenOn"]:
                error = "you may be trying to make a meetup duplicate, please confirm!!"
                abort(make_response(
                    jsonify({"status": 409, "error": error}), 409))

    def show_all_meetups(self):
        """ generate all available meetups """
        if not self.d_b:
            abort(make_response(
                jsonify({"status": 404, "error": "no meetups found"}), 404))
        return self.d_b
