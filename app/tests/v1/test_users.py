""" tests for user endpoints"""

import os
import json
import datetime
import unittest
from app import create_app
KEY = os.getenv("SECRET")

TIME_NOW = datetime.datetime.now()


class BaseTest(unittest.TestCase):
    """Base TestCase for user tests"""

    def setUp(self):
        """ Definig some variables to be used before each test"""
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.usercreate1 = {
            "firstName": "Trevor",
            "lastName": "Kurland",
            "otherName": "Burudi",
            "userName": "trevor",
            "email": "trevbk@gmail.com",
            "phone": "+254712345678",
            "password": "$$22BBkk",
        }
        self.usernametaken = {
            "firstName": "Trevor",
            "lastName": "Kurland",
            "otherName": "Burudi",
            "userName": "trevor",
            "email": "trevbk@gmail.com",
            "phone": "+254712345678",
            "password": "$$22BBkk",
        }
        self.no_username = {
            "firstName": "Trevor",
            "lastName": "Kurland",
            "email": "trevbk@gmail.com",
            "phone": "+254712345678",
            "password": "$$22BBkk",
        }
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
            "regDate": TIME_NOW.strftime("%D"),
            "isAdmin": True
        }
        self.not_confpass = {
            "firstName": "Trevor",
            "lastName": "Kurland",
            "otherName": "Burudi",
            "userName": "trevor",
            "email": "abc@abc.com",
            "phone": "+254712345678",
            "password": "$$22BBkk"
        }
        self.empty_username = {
            "firstName": "Trevor",
            "lastName": "Kurland",
            "otherName": "Burudi",
            "userName": "",
            "email": "abc@abc.com",
            "phone": "+254712345678",
            "password": "$$22BBkk"
        }
        self.empty_fname = {
            "firstName": "",
            "lastName": "Kurland",
            "otherName": "Burudi",
            "userName": "trevor",
            "email": "abc@abc.com",
            "phone": "+254712345678",
            "password": "$$22BBkk"
        }
        self.empty_lname = {
            "firstName": "Trevor",
            "lastName": "",
            "otherName": "Burudi",
            "userName": "trevor",
            "email": "abc@abc.com",
            "phone": "+254712345678",
            "password": "$$22BBkk"
        }
        self.empty_email = {
            "firstName": "Trevor",
            "lastName": "Kurland",
            "otherName": "Burudi",
            "userName": "trevor",
            "email": "",
            "phone": "+254712345678",
            "password": "$$22BBkk"
        }
        self.empty_password = {
            "firstName": "Trevor",
            "lastName": "Kurland",
            "otherName": "Burudi",
            "userName": "trevor",
            "email": "abc@abc.com",
            "phone": "+254712345678",
            "password": ""
        }

        self.empty_phone = {
            "firstName": "Trevor",
            "lastName": "Kurland",
            "otherName": "Burudi",
            "userName": "trevor",
            "email": "abc@abc.com",
            "phone": "",
            "password": "$$22BBkk"
        }
        self.invalid_username = {
            "firstName": "Trevor",
            "lastName": "Kurland",
            "otherName": "Burudi",
            "userName": "^^jjsh",
            "email": "abc@abc.com",
            "phone": "+254712345678",
            "password": "$$22BBkk"
        }
        self.pass_no_caps = {
            "firstName": "Trevor",
            "lastName": "Kurland",
            "otherName": "Burudi",
            "userName": "jjsh",
            "email": "abc@abc.com",
            "phone": "+254712345678",
            "password": "$$22kk"
        }
        self.pass_no_chars = {
            "firstName": "Trevor",
            "lastName": "Kurland",
            "otherName": "Burudi",
            "userName": "jjshhh",
            "email": "abnnc@abc.com",
            "phone": "+254712345678",
            "password": "2BBk"
        }
        self.key_miss = {
            "firstName": "Trevor",
            "userName": "trevor",
            "email": "abc@abc.com",
            "phone": "+254712345678",
            "password": "$$22BBkk"
        }
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
            '/api/v1/signup', data=json.dumps(self.no_username), content_type="application/json")
        sign_resp = json.loads(response.data.decode(
            'utf-8', KEY))
        self.assertEqual(
            sign_resp["error"], "userName field is missing")
        self.assertEqual(response.status_code, 400)

    def test_empty_username_field(self):
        """ test user login when username field is missing """
        response = self.client.post(
            '/api/v1/signup', data=json.dumps(self.empty_username), content_type="application/json")
        sign_resp = json.loads(response.data.decode(
            'utf-8', KEY))
        self.assertEqual(
            sign_resp["error"], "userName cannot be empty!!")
        self.assertEqual(response.status_code, 422)

    def test_empty_firstname_field(self):
        """ test user login when username field is missing """
        response = self.client.post(
            '/api/v1/signup', data=json.dumps(self.empty_fname), content_type="application/json")
        sign_resp = json.loads(response.data.decode(
            'utf-8', KEY))
        self.assertEqual(
            sign_resp["error"], "firstName cannot be empty!!")
        self.assertEqual(response.status_code, 422)

    def test_empty_lastname_field(self):
        """ test user login when username field is missing """
        response = self.client.post(
            '/api/v1/signup', data=json.dumps(self.empty_lname), content_type="application/json")
        sign_resp = json.loads(response.data.decode(
            'utf-8', KEY))
        self.assertEqual(
            sign_resp["error"], "lastName cannot be empty!!")
        self.assertEqual(response.status_code, 422)

    def test_empty_email_field(self):
        """ test user login when username field is missing """
        response = self.client.post(
            '/api/v1/signup', data=json.dumps(self.empty_email), content_type="application/json")
        sign_resp = json.loads(response.data.decode(
            'utf-8', KEY))
        self.assertEqual(
            sign_resp["error"], "email cannot be empty!!")
        self.assertEqual(response.status_code, 422)

    def test_empty_password_field(self):
        """ test user login when username field is missing """
        response = self.client.post(
            '/api/v1/signup', data=json.dumps(self.empty_password), content_type="application/json")
        sign_resp = json.loads(response.data.decode(
            'utf-8', KEY))
        self.assertEqual(
            sign_resp["error"], "password cannot be empty!!")
        self.assertEqual(response.status_code, 422)

    def test_empty_phone_field(self):
        """ test user login when username field is missing """
        response = self.client.post(
            '/api/v1/signup', data=json.dumps(self.empty_phone), content_type="application/json")
        sign_resp = json.loads(response.data.decode(
            'utf-8', KEY))
        self.assertEqual(
            sign_resp["error"], "phone cannot be empty!!")
        self.assertEqual(response.status_code, 422)

    def test_invalid_username(self):
        """ test for invalid username during signup"""
        response = self.client.post(
            '/api/v1/signup', data=json.dumps(self.invalid_username), content_type="application/json")
        sign_resp = json.loads(response.data.decode(
            'utf-8', KEY))
        self.assertEqual(
            sign_resp["error"], "username can only be a letter or _")
        self.assertEqual(response.status_code, 400)

    def test_invalid_email_format(self):
        """ test for invalid email during sign up """
        response = self.client.post(
            '/api/v1/signup', data=json.dumps(self.bad_email), content_type="application/json")
        sign_resp = json.loads(response.data.decode(
            'utf-8', KEY))
        self.assertEqual(
            sign_resp["error"], "invalid email format!!")
        self.assertEqual(response.status_code, 400)

    def test_invalid_pass_no_caps(self):
        """ test for wrong password format (no capital letters)"""
        response = self.client.post(
            '/api/v1/signup', data=json.dumps(self.pass_no_caps), content_type="application/json")
        sign_resp = json.loads(response.data.decode(
            'utf-8', KEY))
        self.assertEqual(
            sign_resp["error"], "password should have number, upper and lower letters + a special character")
        self.assertEqual(response.status_code, 400)

    def test_invalid_pass_no_chars(self):
        """ test for wrong password format with no characters """
        response = self.client.post(
            '/api/v1/signup', data=json.dumps(self.pass_no_chars), content_type="application/json")
        sign_resp = json.loads(response.data.decode(
            'utf-8', KEY))
        self.assertEqual(
            sign_resp["error"], "password should have number, upper and lower letters + a special character")
        self.assertEqual(response.status_code, 400)

    def test_username_taken(self):
        """ test for a user stempt to signup with already taken name """
        response = self.client.post(
            '/api/v1/signup', data=json.dumps(self.usernametaken), content_type="application/json")
        sign_resp = json.loads(response.data.decode(
            'utf-8', KEY))
        self.assertEqual(sign_resp["error"],
                         "user with the username already exists")
        self.assertEqual(response.status_code, 409)

    def test_no_signup_data(self):
        """ test when no signup data is given """
        response = self.client.post(
            '/api/v1/signup', data=json.dumps(self.nodata), content_type="application/json")
        sign_resp = json.loads(response.data.decode(
            'utf-8', KEY))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(sign_resp["error"], "no userdata data!!")


class TestUserLogin(unittest.TestCase):
    """ test for user login"""

    def setUp(self):
        """ creating data for global use"""
        self.app = create_app("testing")
        self.client = self.app.test_client()

        self.user_data_return = {
            "firstName": "Trevor",
            "lastName": "Kurland",
            "otherName": "Burudi",
            "userName": "trevor",
            "email": "trevbk@gmail.com",
            "phone": "+254712345678",
            "password": "$$22BBkk"
        }
        self.userlogin1 = {
            "userlog": "trevor",
            "password": "$$22BBkk"
        }
        self.userlogin2 = {
            "userlog": "trevbk@gmail.com",
            "password": "$$22BBkk"
        }
        self.userlogin3 = {
            "userlog": "zonec",
            "password": "$22BBkk"
        }
        self.userlogin4 = {
            "userlog": "trevbkbk@gmail.com",
            "password": ""
        }
        self.userlogin5 = {
            "userlog": "",
            "password": "trevbkbk@gmail.comBB"
        }
        self.nodata = {}

    def tearDown(self):
        pass

    def test_successful_login_with_username(self):
        """ test user login successfully using username """
        print(os.getenv("SECRET"))
        response = self.client.post(
            '/api/v1/login', data=json.dumps(self.userlogin1), content_type="application/json")
        result = json.loads(response.data.decode("UTF-8"), KEY)
        self.assertEqual(result["message"], "logged in successfully")
        self.assertEqual(response.status_code, 200)

    def test_successful_login_with_email(self):
        """ test user login successfully using email"""
        response = self.client.post(
            '/api/v1/login', data=json.dumps(self.userlogin2), content_type="application/json")
        result = json.loads(response.data.decode("UTF-8"), KEY)
        self.assertEqual(result["message"], "logged in successfully")
        self.assertEqual(response.status_code, 200)

    def test_user_login_fail_user_email(self):
        """ test user login with wrong email input """
        response = self.client.post(
            '/api/v1/login', data=json.dumps(self.userlogin3), content_type="application/json")
        json_response = json.loads(response.data.decode("utf-8"), KEY)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(json_response["error"],
                         "invalid userName or pasword!!")

    def test_login_fail_empty_pass(self):
        """ test when no password parameter/value is given """
        response = self.client.post(
            '/api/v1/login', data=json.dumps(self.userlogin4), content_type="application/json")
        json_response = json.loads(response.data.decode("utf-8"), KEY)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            json_response["error"], "password cannot be empty!!")

    def test_login_fail_empty_userlog(self):
        """ test when userlog parameter/value is given """
        response = self.client.post(
            '/api/v1/login', data=json.dumps(self.userlogin5), content_type="application/json")
        json_response = json.loads(response.data.decode("utf-8"), KEY)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            json_response["error"], "userlog cannot be empty!!")

    def test_empty_login_detail(self):
        """ test when no email data is given """
        response = self.client.post(
            '/api/v1/login', data=json.dumps(self.nodata), content_type="application/json")
        self.assertEqual(response.status_code, 404)
