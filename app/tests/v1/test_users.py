import unittest
from app import my_app
import os
import json
import pytest
import datetime

time_now = datetime.datetime.now()


class BaseTest(unittest.TestCase):
    """Base TestCase for user tests"""

    def setUp(self):
        self.app = my_app
        self.client = self.app.test_client()

        # successful
        self.usercreate1 = {
            "firstName": "Trevor",
            "lastName": "Kurland",
            "otherName": "Burudi",
            "userName": "trevor",
            "email": "trevbk@gmail.com",
            "phone": "+254712345678",
            "password": "$$22BBkk",
        }

        # username taken
        self.usernametaken = {
            "firstName": "Trevor",
            "lastName": "Kurland",
            "otherName": "Burudi",
            "userName": "trevor",
            "email": "trevbk@gmail.com",
            "phone": "+254712345678",
            "password": "$$22BBkk",
        }

        # username missing
        self.big_miss = {
            "firstName": "Trevor",
            "lastName": "Kurland",
            "email": "trevbk@gmail.com",
            "phone": "+254712345678",
            "password": "$$22BBkk",
        }

        self.user_data_return = {
            "id": 1,
            "firstName": "Trevor",
            "lastName": "Kurland",
            "otherName": "Burudi",
            "userName": "trevor",
            "email": "trevbk@gmail.com",
            "phone": "+254712345678",
            "password": "$$22BBkk",
            "regDate": time_now.strftime("%D"),
            "isAdmin": True
        }

        # missing confirmm password
        self.not_confpass = {
            "firstName": "Trevor",
            "lastName": "Kurland",
            "otherName": "Burudi",
            "userName": "trevor",
            "email": "abc@abc.com",
            "phone": "+254712345678",
            "password": "$$22BBkk"
        }

        # missing userName
        self.no_username = {
            "firstName": "Trevor",
            "lastName": "Kurland",
            "otherName": "Burudi",
            "userName": "",
            "email": "abc@abc.com",
            "phone": "+254712345678",
            "password": "$$22BBkk"
        }

        # some key field missing (lastName)
        self.key_miss = {
            "firstName": "Trevor",
            "userName": "trevor",
            "email": "abc@abc.com",
            "phone": "+254712345678",
            "password": "$$22BBkk"
        }

        # login successful username
        self.userlogin1 = {
            "userlog": "zonecc",
            "password": "$22BBkk"
        }

        # login successful failed email
        self.userlogin2 = {
            "userlog": "m_m_m_mm@gmail.com",
            "password": "$22BBkk"
        }

        # login fail username
        self.userlogin3 = {
            "userlog": "zonec",
            "password": "$22BBkk"
        }

        # login fail wrong email
        self.userlogin4 = {
            "userlog": "trevbkbk@gmail.com",
            "password": ""
        }

        # loginand signup fail - no data
        self.nodata = {}

    def tearDown(self):
        pass


class Testusers(BaseTest):
    """Tests user signup and login"""

    def test_signup_successful(self):
        response = self.client.post(
            '/api/v1/signup', data=json.dumps(self.usercreate1), content_type="application/json")
        self.assertEqual(response.status_code, 201)

    def test_missing_key_fields(self):
        response = self.client.post(
            '/api/v1/signup', data=json.dumps(self.big_miss), content_type="application/json")
        sign_resp = json.loads(response.data.decode(
            'utf-8', my_app.config['SECRET_KEY']))
        self.assertEqual(sign_resp["error"], "a key field is missing")
        self.assertEqual(response.status_code, 400)

    def test_empty_major_field(self):
        response = self.client.post(
            '/api/v1/signup', data=json.dumps(self.no_username), content_type="application/json")
        sign_resp = json.loads(response.data.decode(
            'utf-8', my_app.config['SECRET_KEY']))
        self.assertEqual(
            sign_resp["error"], "all fields are required(firstName,lastName,password,userName,phone and email)")
        self.assertEqual(response.status_code, 422)

    def test_username_taken(self):
        response = self.client.post(
            '/api/v1/signup', data=json.dumps(self.usernametaken), content_type="application/json")
        sign_resp = json.loads(response.data.decode(
            'utf-8', my_app.config['SECRET_KEY']))
        self.assertEqual(sign_resp["error"],
                         "user with that name already exists")
        self.assertEqual(response.status_code, 409)

    def test_no_signup_data(self):
        response = self.client.post(
            '/api/v1/signup', data=json.dumps(self.nodata), content_type="application/json")
        self.assertEqual(response.status_code, 204)

    def test_user_login_username_success(self):
        response = self.client.post(
            '/api/v1/login', data=json.dumps(self.userlogin1), content_type="application/json")
        json_response = json.loads(response.data.decode("utf-8"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["data"],
                         "logged in successfully with username")

    def test_user_login_email_success(self):
        response = self.client.post(
            '/api/v1/login', data=json.dumps(self.userlogin2), content_type="application/json")
        json_response = json.loads(response.data.decode("utf-8"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["data"],
                         "logged in successfully with email")

    def test_user_login_fail_user_email(self):
        response = self.client.post(
            '/api/v1/login', data=json.dumps(self.userlogin1), content_type="application/json")
        json_response = json.loads(response.data.decode("utf-8"))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(json_response["data"], "logged in failed")

    def test_empty_login_detail(self):
        response = self.client.post(
            '/api/v1/login', data=json.dumps(self.userlogin1), content_type="application/json")
        json_response = json.loads(response.data.decode("utf-8"))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(json_response["data"], "please fill all fields")
