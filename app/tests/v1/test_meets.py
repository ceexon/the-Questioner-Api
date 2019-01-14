" contains tests for meetup endpoints "

import os
import json
import datetime
import unittest
from app import create_app
from app.api.v1.models.models import MEETUP_LIST
KEY = os.getenv("SECRET")


class BaseTest(unittest.TestCase):
    """ generate data for testing meetup endpoints """

    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()

        target_time = datetime.datetime.now() + datetime.timedelta(days=7)
        target_time = target_time.replace(microsecond=0)

        self.admin_user = {
            "firstName": "Trevor",
            "lastName": "Kurland",
            "otherName": "Burudi",
            "userName": "admin",
            "email": "admin@gmail.com",
            "phone": "+254712345678",
            "password": "$$22BBkk",
        }

        self.admin_login = {
            "userlog": "admin",
            "password": "$$22BBkk"
        }

        self.local_user = {
            "firstName": "Trevor",
            "lastName": "Kurland",
            "otherName": "Burudi",
            "userName": "local",
            "email": "local@gmail.com",
            "phone": "+254712345678",
            "password": "$$22BBkk",
        }

        self.local_login = {
            "userlog": "local",
            "password": "$$22BBkk"
        }

        self.meetup_data = {
            "topic": "My first meetup",
            "images": ["/home/zonecc/pictures/img1.png", "/home/zonecc/picturesimg2/png"],
            "location": "Home",
            "happenOn": "2/04/2919",
            "tags": ["#At home", "#coding", "#enjoy"]
        }

        self.meetup_data_2 = {
            "topic": "My first meetup 22",
            "images": ["/home/zonecc/pictures/img1.png", "/home/zonecc/picturesimg2/png"],
            "location": "Home study",
            "happenOn": "2/04/2919",
            "tags": ["#At home", "#coding", "#enjoy"]
        }

        self.meetup_data_4 = {
            "topic": "",
            "images": ["/home/zonecc/pictures/img1.png", "/home/zonecc/picturesimg2/png"],
            "location": "Home study",
            "happenOn": "2/04/2919",
            "tags": ["#At home", "#coding", "#enjoy"]
        }

        self.meetup_data_5 = {
            "topic": "      ",
            "images": ["/home/zonecc/pictures/img1.png", "/home/zonecc/picturesimg2/png"],
            "location": "Home study",
            "happenOn": "2/04/2919",
            "tags": ["#At home", "#coding", "#enjoy"]
        }

        self.meetup_data_3 = {
            "images": ["/home/zonecc/pictures/img1.png", "/home/zonecc/picturesimg2/png"],
            "location": "Home study 1",
            "happenOn": "2/04/2919",
            "tags": ["#At home", "#coding", "#enjoy"]
        }

        self.meetup_data_6 = {
            "tags": ["      ", "#some_other_tag"],
            "images": ["/home/zonecc/pictures/img1.png", "/home/zonecc/picturesimg2/png"],
            "location": "Home study",
            "happenOn": "2/04/2919",
            "topic": "#At home #coding #enjoy"
        }

        self.meetup_data_7 = {
            "tags": [],
            "images": ["/home/zonecc/pictures/img1.png", "/home/zonecc/picturesimg2/png"],
            "location": "Home study",
            "happenOn": "2/04/2919",
            "topic": "#At home #coding #enjoy"
        }

        self.meetup_data_8 = {
            "images": ["/home/zonecc/pictures/img1.png", "/home/zonecc/picturesimg2/png"],
            "location": "Home study",
            "happenOn": "2/04/2919",
            "topic": "#At home #coding #enjoy"
        }

        self.meetup_data_9 = {
            "topic": "My first meetup 22",
            "images": ["/home/zonecc/pictures/img1.png", "/home/zonecc/picturesimg2/png"],
            "happenOn": "2/04/2919",
            "tags": ["#At home", "#coding", "#enjoy"]
        }

        self.meetup_data_10 = {
            "topic": "My first meetup 22",
            "images": ["/home/zonecc/pictures/img1.png", "/home/zonecc/picturesimg2/png"],
            "location": "Home study",
            "happenOn": "",
            "tags": ["#At home", "#coding", "#enjoy"]
        }

    def tearDown(self):
        pass


class TestMeetups(BaseTest):
    """ tests meetups endpoint and edge-cases"""
    token = ""

    def login(self):
        self.client.post(
            '/api/v1/signup', data=json.dumps(self.admin_user), content_type="application/json")
        login = self.client.post(
            '/api/v1/login', data=json.dumps(self.admin_login), content_type="application/json")
        self.token = json.loads(login.data.decode('utf-8', KEY))
        self.token = self.token["token"]
        return self.token

    def test_1_an_admin_user_can_create_a_meetup(self):
        """
        Test that a user can enter meetup details and create a meetup
        """
        self.token = self.login()
        response = self.client.post("api/v1/meetups", data=json.dumps(self.meetup_data), headers={
                                    'x-access-token': self.token}, content_type="application/json")
        result = json.loads(response.data.decode("utf-8"))
        self.assertTrue(result["data"])
        self.assertEqual(response.status_code, 201)

    def test_1_an_id_for_metup_valid_but_no_token_get(self):
        """ test when a user with no token attempts to access a single meetup """
        response = self.client.get("api/v1/meetups/1")
        result = json.loads(response.data.decode("utf-8"))
        self.assertEqual(result["error"], "Token is missing")
        self.assertEqual(response.status_code, 401)

    def test_1_an_id_for_metup_invalid_with_token(self):
        self.token = self.login()
        """ test when a user with a token attempts to access a single meetup but with invalid id"""
        response = self.client.get(
            "api/v1/meetups/10", headers={'x-access-token': self.token})
        result = json.loads(response.data.decode("utf-8"))
        self.assertEqual(
            result["error"], "requested id was not found or is out of range")
        self.assertEqual(response.status_code, 404)

    def test_1_an_id_for_metup_valid_with_token(self):
        """ test when a user with token attempts to access a single meetup successfully"""
        self.token = self.login()
        response = self.client.get(
            "api/v1/meetups/1", headers={'x-access-token': self.token})
        result = json.loads(response.data.decode("utf-8"))
        self.assertTrue(result["data"])
        self.assertEqual(response.status_code, 200)

    def test_2_an_admin_user_attempt_to_duplicate_meetup(self):
        """
        Test that a user can enter meetup details and create a meetup
        """
        self.token = self.login()
        response = self.client.post("api/v1/meetups", data=json.dumps(self.meetup_data), headers={
                                    'x-access-token': self.token}, content_type="application/json")
        duplicate = json.loads(response.data.decode("utf-8"))
        self.assertEqual(
            duplicate["error"], "you may be trying to make a meetup duplicate, please confirm!!")
        self.assertEqual(response.status_code, 409)

    def test_3_local_user_try_to_create_meetup(self):
        """ local user attempts to create a meetup """
        self.token = self.login()
        self.client.post(
            '/api/v1/signup', data=json.dumps(self.local_user), content_type="application/json")
        local = self.client.post(
            '/api/v1/login', data=json.dumps(self.local_login), content_type="application/json")
        local_tk = json.loads(local.data.decode('utf-8', KEY))
        l_token = local_tk["token"]
        response = self.client.post("api/v1/meetups", data=json.dumps(self.meetup_data_2), headers={
                                    'x-access-token': l_token}, content_type="application/json")
        forbid = json.loads(response.data.decode("utf-8"))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(forbid["error"], "you cannot create a meetup")

    def test_5_token_missing_try_to_create_meetup(self):
        response = self.client.post(
            "api/v1/meetups", data=json.dumps(self.meetup_data_2), content_type="application/json")
        not_allowed = json.loads(response.data.decode("utf-8"))
        self.assertEqual(not_allowed["error"], "Token is missing")
        self.assertEqual(response.status_code, 401)

    def test_6_missing_topic(self):
        """ test when topic required field is midding """
        self.token = self.login()
        response = self.client.post("api/v1/meetups", data=json.dumps(self.meetup_data_3), headers={
                                    'x-access-token': self.token}, content_type="application/json")
        result = json.loads(response.data.decode("utf-8"))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["error"], "topic field is missing")

    def test_7_empty_topic(self):
        """ test when topic required field is midding """
        self.token = self.login()
        response = self.client.post("api/v1/meetups", data=json.dumps(self.meetup_data_4), headers={
                                    'x-access-token': self.token}, content_type="application/json")
        result = json.loads(response.data.decode("utf-8"))
        self.assertEqual(response.status_code, 422)
        self.assertEqual(result["error"], "topic cannot be empty!!")

    def test_8_whitespace_only_topic(self):
        """ test when topic required field is midding """
        self.token = self.login()
        response = self.client.post("api/v1/meetups", data=json.dumps(self.meetup_data_5), headers={
                                    'x-access-token': self.token}, content_type="application/json")
        result = json.loads(response.data.decode("utf-8"))
        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            result["error"], "topic cannot contain whitespace only")

    def test_9_whitespace_only_tags(self):
        """ test when topic required field is midding """
        self.token = self.login()
        response = self.client.post("api/v1/meetups", data=json.dumps(self.meetup_data_6), headers={
                                    'x-access-token': self.token}, content_type="application/json")
        result = json.loads(response.data.decode("utf-8"))
        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            result["error"], "tag input cannot be empty whitespace!!")

    def test_10_empty_tags(self):
        """ test when topic required field is midding """
        self.token = self.login()
        response = self.client.post("api/v1/meetups", data=json.dumps(self.meetup_data_7), headers={
                                    'x-access-token': self.token}, content_type="application/json")
        result = json.loads(response.data.decode("utf-8"))
        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            result["error"], "at least 1 tag is required[#name_of_tag]")

    def test_11_missing_tags(self):
        """ test when topic required field is midding """
        self.token = self.login()
        response = self.client.post("api/v1/meetups", data=json.dumps(self.meetup_data_8), headers={
                                    'x-access-token': self.token}, content_type="application/json")
        result = json.loads(response.data.decode("utf-8"))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            result["error"], "tag field is missing")

    def test_12_missing_location(self):
        """ test when topic required field is midding """
        self.token = self.login()
        response = self.client.post("api/v1/meetups", data=json.dumps(self.meetup_data_9), headers={
                                    'x-access-token': self.token}, content_type="application/json")
        result = json.loads(response.data.decode("utf-8"))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            result["error"], "location field is missing")

    def test_12_happen_on_empty(self):
        """ test when topic required field is midding """
        self.token = self.login()
        response = self.client.post("api/v1/meetups", data=json.dumps(self.meetup_data_10), headers={
                                    'x-access-token': self.token}, content_type="application/json")
        result = json.loads(response.data.decode("utf-8"))
        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            result["error"], "happenOn cannot be empty!!")

    def test_13_get_all_meetups_none_found(self):
        response = self.client.get("api/v1/meetups")
        self.assertEqual(response.status_code, 404)

    def test_41_get_all_upcoming_meetups(self):
        MEETUP_LIST.append(self.meetup_data)
        response = self.client.get("api/v1/meetups/upcoming")
        result = json.loads(response.data.decode("utf-8"))
        self.assertTrue(result["data"])
        self.assertEqual(response.status_code, 200)

    def test_20_get_all_upcoming_meetups(self):
        response = self.client.get("api/v1/meetups")
        result = json.loads(response.data.decode("utf-8"))
        self.assertTrue(result["data"])
        self.assertEqual(response.status_code, 200)

    def test_delete_1_meetup_invalid_id(self):
        """ tests  when an admin users try to delete meetup with invalid id but correct format """
        self.token = self.login()
        response = self.client.delete(
            "/api/v1/meetups/10", headers={'x-access-token': self.token})
        not_found = json.loads(response.data.decode("utf-8"))
        self.assertEqual(
            not_found["error"], "requested id was not found or is out of range")
        self.assertEqual(response.status_code, 404)

    def test_delete_1_meetup_invalid_id_format(self):
        """ tests  when an admin users try to delete meetup with invalid id format """
        self.token = self.login()
        response = self.client.delete(
            "/api/v1/meetups/tty", headers={'x-access-token': self.token})
        not_found = json.loads(response.data.decode("utf-8"))
        self.assertEqual(
            not_found["error"], "the id you parsed in invalid, can only be a number")
        self.assertEqual(response.status_code, 400)

    def test_delete_2_meetup_successfully(self):
        """ tests when an admin user attempts to delete a meetup with correct id"""
        self.token = self.login()
        response = self.client.delete(
            "/api/v1/meetups/1", headers={'x-access-token': self.token})
        result = json.loads(response.data.decode("utf-8"))
        self.assertTrue(result["data"])
        self.assertEqual(response.status_code, 200)
