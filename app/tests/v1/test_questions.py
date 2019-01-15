import unittest
from app import create_app
import os
import json
import pytest
import datetime
from app.api.v1.models.models import QUESTION_LIST, MEETUP_LIST
from ...api.v1.utils.validations import token_required
KEY = os.getenv("SECRET")


class TestQuestions(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()

        self.admin_user = {
            "firstName": "Trevor",
            "lastName": "Kurland",
            "otherName": "Burudi",
            "userName": "admin",
            "email": "admin@gmail.com",
            "phone": "+254712345678",
            "password": "$$22BBkk",
        }

        self.meetup_data = {
            "topic": "My first meetup",
            "images": ["/home/zonecc/pictures/img1.png", "/home/zonecc/picturesimg2/png"],
            "location": "Home",
            "happenOn": "2/04/2919",
            "tags": ["#At home", "#coding", "#enjoy"],
            "id": 2
        }

        self.admin_login = {
            "userlog": "admin",
            "password": "$$22BBkk"
        }

        self.question1 = {}

        self.question2 = {
            "topic": "no body",
            "body": ""
        }

        self.question5 = {
            "topic": "no body",
            "body": "    "
        }

        self.question3 = {
            "body": "uukskuhsh"
        }

        self.question4 = {
            "body": "some body",
            "topic": "meet topic"
        }

        self.posted_question = {
            "body": "some body",
            "createOn": "01/15/19",
            "downvotes": 0,
            "id": 4,
            "meetup": 3,
            "topic": "meet topic",
            "upvotes": 0,
            "user": 3
        }

    def tearDown(self):
        pass

    def login(self):
        self.client.post(
            '/api/v1/signup', data=json.dumps(self.admin_user), content_type="application/json")
        login = self.client.post(
            '/api/v1/login', data=json.dumps(self.admin_login), content_type="application/json")
        self.token = json.loads(login.data.decode('utf-8', KEY))
        MEETUP_LIST.append(self.meetup_data)
        self.token = self.token["token"]
        return self.token

    def test__user_asks_a_question(self):
        """
        Test that a user can ask a question
        """
        self.token = self.login()
        response = self.client.post("/api/v1/meetups/2/questions", data=json.dumps(self.question4), headers={
                                    'x-access-token': self.token}, content_type="application/json")
        result = json.loads(response.data.decode("utf-8"))
        self.assertTrue(result["Question"])
        self.assertEqual(response.status_code, 201)

    def test__user_asks_a_question_invalid_meetup_id(self):
        """
        Test that a user can ask a question
        """
        self.token = self.login()
        response = self.client.post("/api/v1/meetups/8/questions", data=json.dumps(self.question4), headers={
            'x-access-token': self.token}, content_type="application/json")
        result = json.loads(response.data.decode("utf-8"))
        self.assertEqual(
            result["error"], "requested id was not found or is out of range")
        self.assertEqual(response.status_code, 404)

    def test_test_question_missing_topic(self):
        """
        Test that a user can ask a question
        """
        self.token = self.login()
        response = self.client.post("/api/v1/meetups/2/questions", data=json.dumps(self.question3), headers={
            'x-access-token': self.token}, content_type="application/json")
        result = json.loads(response.data.decode("utf-8"))
        self.assertEqual(
            result["error"], "topic field is missing")
        self.assertEqual(response.status_code, 400)

    def test_test_question_empty_body(self):
        """
        Test that a user can ask a question
        """
        self.token = self.login()
        response = self.client.post("/api/v1/meetups/2/questions", data=json.dumps(self.question2), headers={
            'x-access-token': self.token}, content_type="application/json")
        result = json.loads(response.data.decode("utf-8"))
        self.assertEqual(
            result["error"], "body cannot be empty!!")
        self.assertEqual(response.status_code, 422)

    def test_test_question_whitespace_body(self):
        """
        Test that a user can ask a question
        """
        self.token = self.login()
        response = self.client.post("/api/v1/meetups/2/questions", data=json.dumps(self.question5), headers={
            'x-access-token': self.token}, content_type="application/json")
        result = json.loads(response.data.decode("utf-8"))
        self.assertEqual(
            result["error"], "body cannot contain whitespace only")
        self.assertEqual(response.status_code, 422)

    def test_test_question_no_data(self):
        """
        Test that a user can ask a question
        """
        self.token = self.login()
        response = self.client.post("/api/v1/meetups/2/questions", headers={
            'x-access-token': self.token}, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test__user_asks_gets_all_questions_for_a_meetup(self):
        """
        Test that a user can get all questions asked for a given meetup
        """
        self.token = self.login()
        response = self.client.get("/api/v1/meetups/2/questions", data=json.dumps(self.question4), headers={
            'x-access-token': self.token}, content_type="application/json")
        result = json.loads(response.data.decode("utf-8"))
        self.assertTrue(result["Questions"])
        self.assertEqual(response.status_code, 200)

    def test__user_asks_gets_all_questions_for_a_meetup_by_id(self):
        """
        Test that a user can get a question from a meetup by id
        """
        self.token = self.login()
        response = self.client.get("/api/v1/meetups/2/questions/1", data=json.dumps(self.question4), headers={
            'x-access-token': self.token}, content_type="application/json")
        result = json.loads(response.data.decode("utf-8"))
        self.assertTrue(result["Question"])
        self.assertEqual(response.status_code, 200)

    def test_user_votes_for_question(self):
        """
        Test that a user can upvote for a question from a meetup
        """
        self.token = self.login()
        response = self.client.patch("/api/v1/meetups/1/questions/1/upvote", data=json.dumps(self.question4), headers={
            'x-access-token': self.token}, content_type="application/json")
        result = json.loads(response.data.decode("utf-8"))
        self.assertTrue(result["Question"])
        self.assertEqual(response.status_code, 201)

    def test_user_votes_for_question_again(self):
        """
        Test that a user can upvote for a question from a meetup again
        """
        self.token = self.login()
        response = self.client.patch("/api/v1/meetups/1/questions/1/upvote", data=json.dumps(self.question4), headers={
            'x-access-token': self.token}, content_type="application/json")
        result = json.loads(response.data.decode("utf-8"))
        self.assertEqual(result["message"], "You cannot vote more than once")
        self.assertEqual(response.status_code, 403)
