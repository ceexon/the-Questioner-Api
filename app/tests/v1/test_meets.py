import unittest
from app import create_app
import os
import json
import pytest
import datetime
from app.api.v1.models.models import MEETUP_LIST


class BaseTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()

        target_time = datetime.datetime.now() + datetime.timedelta(days=7)
        target_time = target_time.replace(microsecond=0)
        today_now = datetime.datetime.now()

        self.meetup1 = {
            "topic": "My first meetup",
            "images": ["/home/zonecc/pictures/img1.png", "/home/zonecc/picturesimg2/png"],
            "location": "Home",
            "happenOn": target_time.strftime("%D %H:%M %p"),
            "tags": ["#At home", "#coding", "#enjoy"]
        }

        self.meetup11 = {
            "topic": "",
            "images": ["/home/zonecc/pictures/img1.png", "/home/zonecc/picturesimg2/png"],
            "location": "Home",
            "happenOn": target_time.strftime("%D %H:%M %p"),
            "tags": ["#At home", "#coding", "#enjoy"]
        }

        self.meetup1created = {
            "id": 1,
            "createOn": today_now.strftime("%d %h %Y"),
            "topic": "My first meetup",
            "images": ["/home/zonecc/pictures/img1.png", "/home/zonecc/picturesimg2/png"],
            "location": "Home",
            "happenOn": target_time.strftime("%D %H:%M %p"),
            "tags": ["#At home", "#coding", "#enjoy"]
        }

        self.meetup2 = {
            "images": ["/home/zonecc/pictures/img1.png", "/home/zonecc/picturesimg2/png"],
            "location": "Home",
            "happenOn": target_time.strftime("%D %H:%M %p"),
            "tags": ["#At home", "#coding", "#enjoy"]
        }

        self.nodata = {}

    def tearDown(self):
        pass


class TestMeetup(BaseTest):
    def test_created_meetup_success(self):
        response = self.client.post(
            '/api/v1/meetups', data=json.dumps(self.meetup1), content_type="application/json")
        meet_resp = json.loads(response.data.decode(
            'utf-8', self.app.config['SECRET_KEY']))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(meet_resp["data"], self.meetup1created)

    def test_create_meetup_fail_no_data(self):
        response = self.client.post(
            '/api/v1/meetups', data=json.dumps(self.nodata), content_type="application/json")
        self.assertEqual(response.status_code, 404)

    def test_get_all_meetups_success(self):
        MEETUP_LIST.append(self.meetup1created)
        response = self.client.get(
            '/api/v1/meetups', data=json.dumps(self.meetup1), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_get_all_upcoming_success(self):
        MEETUP_LIST.append(self.meetup1created)
        response = self.client.get(
            '/api/v1/meetups/upcoming', data=json.dumps(self.meetup1), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_get_single_meetup_success(self):
        MEETUP_LIST.append(self.meetup1created)
        response = self.client.get(
            '/api/v1/meetups/1', data=json.dumps(self.meetup1), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_get_single_meetup_fail(self):
        MEETUP_LIST.append(self.meetup1created)
        response = self.client.get(
            '/api/v1/meetups/1000', data=json.dumps(self.meetup1), content_type="application/json")
        self.assertEqual(response.status_code, 404)

    def test_delete_meetup_fail(self):
        response = self.client.delete(
            '/api/v1/meetups/1000', data=json.dumps(self.meetup1), content_type="application/json")
        self.assertEqual(response.status_code, 404)

    def test_delete_meetup_success(self):
        response = self.client.delete(
            '/api/v1/meetups/1', data=json.dumps(self.meetup1), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_delete_meetup_fail(self):
        response = self.client.delete(
            '/api/v1/meetups/1000', data=json.dumps(self.meetup1), content_type="application/json")
        self.assertEqual(response.status_code, 404)

    def test_delete_meetup_success(self):
        response = self.client.delete(
            '/api/v1/meetups/1', data=json.dumps(self.meetup1), content_type="application/json")
        self.assertEqual(response.status_code, 200)
