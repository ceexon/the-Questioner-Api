import unittest
from app import create_app
from app.api.v1.models.models import Users
import os
import json
import pytest
import datetime

time_now = datetime.datetime.now()


class BaseTest(unittest.TestCase):
    """Base TestCase for user tests"""

    def setUp(self):
        """ Definig some variables to be used before each test"""
        self.app = create_app("testing")
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

        # bad email
        self.bad_email = {
            "firstName": "Trevor",
            "lastName": "Kurland",
            "userName": "trevor__",
            "email": "trevbkail.com",
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

        # empty userName
        self.no_username = {
            "firstName": "Trevor",
            "lastName": "Kurland",
            "otherName": "Burudi",
            "userName": "",
            "email": "abc@abc.com",
            "phone": "+254712345678",
            "password": "$$22BBkk"
        }

        # invalid userName
        self.invalid_username = {
            "firstName": "Trevor",
            "lastName": "Kurland",
            "otherName": "Burudi",
            "userName": "^^jjsh",
            "email": "abc@abc.com",
            "phone": "+254712345678",
            "password": "$$22BBkk"
        }

        # invalid userName
        self.pass_no_caps = {
            "firstName": "Trevor",
            "lastName": "Kurland",
            "otherName": "Burudi",
            "userName": "jjsh",
            "email": "abc@abc.com",
            "phone": "+254712345678",
            "password": "$$22kk"
        }

        # invalid userName
        self.pass_no_chars = {
            "firstName": "Trevor",
            "lastName": "Kurland",
            "otherName": "Burudi",
            "userName": "jjsh",
            "email": "abc@abc.com",
            "phone": "+254712345678",
            "password": "2BB2kk"
        }

        # some key field missing (lastName)
        self.key_miss = {
            "firstName": "Trevor",
            "userName": "trevor",
            "email": "abc@abc.com",
            "phone": "+254712345678",
            "password": "$$22BBkk"
        }

        # loginand signup fail - no data
        self.nodata = {}

    def tearDown(self):
        pass


class TestUserSignUp(BaseTest):
    """Tests user signup and login"""

    def test_a_signup_successful(self):
        """ Test for a successful user registration"""
        response = self.client.post(
            '/api/v1/signup', data=json.dumps(self.usercreate1), content_type="application/json")
        self.assertEqual(response.status_code, 201)

    def test_missing_key_fields(self):
        """ Test when a required field is missing """
        response = self.client.post(
            '/api/v1/signup', data=json.dumps(self.big_miss), content_type="application/json")
        sign_resp = json.loads(response.data.decode(
            'utf-8', self.app.config['SECRET_KEY']))
        self.assertEqual(
            sign_resp["error"], "For a successful signup ensure you input(firstName, lastName, userName, email, phone and password)")
        self.assertEqual(response.status_code, 400)

    def test_empty_major_field(self):
        response = self.client.post(
            '/api/v1/signup', data=json.dumps(self.no_username), content_type="application/json")
        sign_resp = json.loads(response.data.decode(
            'utf-8', self.app.config['SECRET_KEY']))
        self.assertEqual(
            sign_resp["error"], "username cannot be empty!!")
        self.assertEqual(response.status_code, 422)

    def test_invalid_username(self):
        response = self.client.post(
            '/api/v1/signup', data=json.dumps(self.invalid_username), content_type="application/json")
        sign_resp = json.loads(response.data.decode(
            'utf-8', self.app.config['SECRET_KEY']))
        self.assertEqual(
            sign_resp["error"], "username can only contain a number,letter and _")
        self.assertEqual(response.status_code, 400)

    def test_invalid_email_format(self):
        response = self.client.post(
            '/api/v1/signup', data=json.dumps(self.bad_email), content_type="application/json")
        sign_resp = json.loads(response.data.decode(
            'utf-8', self.app.config['SECRET_KEY']))
        self.assertEqual(
            sign_resp["error"], "invalid email format")
        self.assertEqual(response.status_code, 400)

    def test_invalid_pass_no_caps(self):
        response = self.client.post(
            '/api/v1/signup', data=json.dumps(self.pass_no_caps), content_type="application/json")
        sign_resp = json.loads(response.data.decode(
            'utf-8', self.app.config['SECRET_KEY']))
        self.assertEqual(
            sign_resp["error"], "password has no uppercase letter")
        self.assertEqual(response.status_code, 400)

    def test_invalid_pass_no_chars(self):
        response = self.client.post(
            '/api/v1/signup', data=json.dumps(self.pass_no_chars), content_type="application/json")
        sign_resp = json.loads(response.data.decode(
            'utf-8', self.app.config['SECRET_KEY']))
        self.assertEqual(
            sign_resp["error"], "password has no special character(*@#$)")
        self.assertEqual(response.status_code, 400)

    def test_username_taken(self):
        response = self.client.post(
            '/api/v1/signup', data=json.dumps(self.usernametaken), content_type="application/json")
        sign_resp = json.loads(response.data.decode(
            'utf-8', self.app.config['SECRET_KEY']))
        self.assertEqual(sign_resp["error"],
                         "user with that name already exists")
        self.assertEqual(response.status_code, 409)

    def test_no_signup_data(self):
        response = self.client.post(
            '/api/v1/signup', data=json.dumps(self.nodata), content_type="application/json")
        self.assertEqual(response.status_code, 204)


class TestUserLogin(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()

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

        global Users
        Users.append(self.user_data_return)

        # login successful username
        self.userlogin1 = {
            "userlog": "trevor",
            "password": "$$22BBkk"
        }

        # login successful failed email
        self.userlogin2 = {
            "userlog": "trevbk@gmail.com",
            "password": "$$22BBkk"
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

    def test_user_login_username_success(self):
        response = self.client.post(
            '/api/v1/login', data=json.dumps(self.userlogin1), content_type="application/json")
        json_response = json.loads(response.data.decode("utf-8"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["data"],
                         "logged in successfully")

    def test_user_login_email_success(self):
        response = self.client.post(
            '/api/v1/login', data=json.dumps(self.userlogin2), content_type="application/json")
        json_response = json.loads(response.data.decode("utf-8"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["data"],
                         "logged in successfully")

    def test_user_login_fail_user_email(self):
        response = self.client.post(
            '/api/v1/login', data=json.dumps(self.userlogin3), content_type="application/json")
        json_response = json.loads(response.data.decode("utf-8"))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(json_response["data"], "invalid login credentials")

    def test_user_login_fail_user_email_cred(self):
        response = self.client.post(
            '/api/v1/login', data=json.dumps(self.userlogin4), content_type="application/json")
        json_response = json.loads(response.data.decode("utf-8"))
        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            json_response["error"], "all fields are required(password,userlog(userName/email))")

    def test_empty_login_detail(self):
        response = self.client.post(
            '/api/v1/login', data=json.dumps(self.nodata), content_type="application/json")
        self.assertEqual(response.status_code, 204)
