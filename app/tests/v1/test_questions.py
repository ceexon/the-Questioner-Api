import unittest
from app import my_app
import os
import json
import pytest
import datetime
from app.api.v1.models.models import Questions


class TestQuestions(unittest.TestCase):
    def setUp(self):
        self.app = my_app
        self.client = self.app.test_client()

        self.question1 = {}

        self.question2 = {
            "topic": "no body",
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
            '/api/v1/questions', data=json.dumps(self.question4), content_type="application/json")
        q_resp = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(q_resp["data"], "question added successfully")

    def test_question_with_no_data(self):
        response = self.client.post(
            '/api/v1/questions', data=json.dumps(self.question1), content_type="application/json")
        self.assertEqual(response.status_code, 204)

    def test_question_with_empty_fields(self):
        response = self.client.post(
            '/api/v1/questions', data=json.dumps(self.question2), content_type="application/json")
        q_resp = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 422)
        self.assertEqual(q_resp["error"],
                         "These fields are required(topic,body)")

    def test_question_missing_key_fields(self):
        response = self.client.post(
            '/api/v1/questions', data=json.dumps(self.question3), content_type="application/json")
        q_resp = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(q_resp["error"], "a key field is missing")

    def test_upvote_question_success(self):
        response = self.client.patch(
            '/api/v1/questions/1/upvote')
        q_resp = json.loads(response.data.decode(
            'utf-8', my_app.config['SECRET_KEY']))
        self.assertEqual(response.status_code, 202)
        self.assertEqual(q_resp["data"], "You have accepted this question")

    def test_downvote_question_success(self):
        Questions.append({"id": 1, "topic": "my first", "body": "no body"})
        response = self.client.patch(
            '/api/v1/questions/1/downvote')
        q_resp = json.loads(response.data.decode(
            'utf-8', my_app.config['SECRET_KEY']))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(q_resp["data"], "You have rejected this question")

    def test_upvote_question_fail(self):
        response = self.client.patch(
            '/api/v1/questions/100/upvote')
        q_resp = json.loads(response.data.decode(
            'utf-8', my_app.config['SECRET_KEY']))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(q_resp["error"], "question not found")
