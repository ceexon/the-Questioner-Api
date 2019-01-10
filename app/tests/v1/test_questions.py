import unittest
from app import my_app
import os
import json
import pytest
import datetime


class TestQuestions(unittest.TestCase):
    def setUp(self):
        self.app = my_app
        self.client = self.app.test_client()

        self.question1 = {}

        self.question2 = {
            "title": "no body",
            "body": ""
        }

        self.question3 = {
            "body": "uukskuhsh"
        }

        self.question4 = {
            "body": "some body",
            "topic": "meet topic"
        }

    def tearDown(self):
        pass

    def test_post_question_success(self):
        response = self.client.post(
            '/api/v1/question: ', data=json.dumps(self.question4), content_type="application/json")
        meet_resp = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(meet_resp["data"], "question added successfully")

    def test_question_with_no_data(self):
        response = self.client.post(
            '/api/v1/question: ', data=json.dumps(self.question1), content_type="application/json")
        meet_resp = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(meet_resp["error"], "no question data found")

    def test_question_with_empty_fields(self):
        response = self.client.post(
            '/api/v1/question: ', data=json.dumps(self.question2), content_type="application/json")
        meet_resp = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 422)
        self.assertEqual(meet_resp["error"], "please fill all fields")

    def test_question_missing_key_fields(self):
        response = self.client.post(
            '/api/v1/question: ', data=json.dumps(self.question2), content_type="application/json")
        meet_resp = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(meet_resp["error"], "missing a topic or a body")

    def test_upvote_question_success(self):
        response = self.client.patch(
            '/api/v1/question/1/upvote')
        meet_resp = json.loads(response.data.decode(
            'utf-8', my_app.config['SECRET_KEY']))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(meet_resp["data"], "upvoted")

    def test_downvote_question_success(self):
        response = self.client.patch(
            '/api/v1/question/1/upvote')
        meet_resp = json.loads(response.data.decode(
            'utf-8', my_app.config['SECRET_KEY']))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(meet_resp["data"], "downvoted")

    def test_upvote_question_fail(self):
        response = self.client.patch(
            '/api/v1/question/100/upvote')
        meet_resp = json.loads(response.data.decode(
            'utf-8', my_app.config['SECRET_KEY']))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(meet_resp["error"], "question not found")
