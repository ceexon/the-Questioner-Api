import unittest
from app import create_app
import os
import json
import pytest
import datetime
from app.api.v1.models.models import MEETUP_LIST
KEY = os.getenv("SECRET")


class BaseTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()

        target_time = datetime.datetime.now() + datetime.timedelta(days=7)
        target_time = target_time.replace(microsecond=0)

        self.meetup1 = {
            "topic": "My first meetup",
            "images": ["/home/zonecc/pictures/img1.png", "/home/zonecc/picturesimg2/png"],
            "location": "Home",
            "happenOn": "2/04/2919",
            "tags": ["#At home", "#coding", "#enjoy"]
        }

        self.meetup11 = {
            "topic": "",
            "images": ["/home/zonecc/pictures/img1.png", "/home/zonecc/picturesimg2/png"],
            "location": "Home",
            "happenOn": "2/02/2019",
            "tags": ["#At home", "#coding", "#enjoy"]
        }

        self.meetup1created = {
            "id": 1,
            "topic": "My first meetup",
            "images": ["/home/zonecc/pictures/img1.png", "/home/zonecc/picturesimg2/png"],
            "location": "Home",
            "happenOn": target_time.strftime("%D"),
            "tags": ["#At home", "#coding", "#enjoy"]
        }

        self.meetup_no_tags = {
            "id": 1,
            "topic": "My first meetup 1",
            "images": ["/home/zonecc/pictures/img1.png", "/home/zonecc/picturesimg2/png"],
            "location": "Homey",
            "happenOn": target_time.strftime("%D")
        }

        self.meetup_no_tags_details = {
            "id": 1,
            "topic": "My first meetup 1",
            "images": ["/home/zonecc/pictures/img1.png", "/home/zonecc/picturesimg2/png"],
            "location": "Homey",
            "happenOn": target_time.strftime("%D"),
            "tags": []
        }

        self.meetup_whitespace_in_tag = {
            "id": 1,
            "topic": "My first meetup 1",
            "images": ["/home/zonecc/pictures/img1.png", "/home/zonecc/picturesimg2/png"],
            "location": "Homey",
            "happenOn": target_time.strftime("%D"),
            "tags": ["#ok", "     "]
        }

        self.meetup2 = {
            "images": ["/home/zonecc/pictures/img1.png", "/home/zonecc/picturesimg2/png"],
            "location": "Home",
            "happenOn": target_time.strftime("%D"),
            "tags": ["#At home", "#coding", "#enjoy"]
        }

        self.meetup21 = {
            "images": ["/home/zonecc/pictures/img1.png", "/home/zonecc/picturesimg2/png"],
            "location": "Home",
            "happenOn": target_time.strftime("%D"),
            "tags": ["#At home", "#coding", "#enjoy"],
            "topic": "       "
        }

        self.meetup211 = {
            "images": ["/home/zonecc/pictures/img1.png", "/home/zonecc/picturesimg2/png"],
            "location": "Home",
            "happenOn": target_time.strftime("%D"),
            "tags": ["#At home", "#coding", "#enjoy"],
            "topic": ""
        }

        self.nodata = {}

    def tearDown(self):
        pass


class TestMeetup(BaseTest):
    def test_created_meetup_success(self):
        response = self.client.post(
            '/api/v1/meetups', data=json.dumps(self.meetup1), content_type="application/json")
        self.assertEqual(response.status_code, 201)

    def test_create_meetup_fail_no_data(self):
        response = self.client.post(
            '/api/v1/meetups', data=json.dumps(self.nodata), content_type="application/json")
        meet_resp = json.loads(response.data.decode(
            'utf-8', KEY))
        self.assertEqual(meet_resp["error"], "No meetup data found")
        self.assertEqual(response.status_code, 400)

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

    def test_get_by_id_out_of_range(self):
        MEETUP_LIST.append(self.meetup1created)
        response = self.client.get(
            '/api/v1/meetups/str', data=json.dumps(self.meetup1), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_get_single_meetup_success(self):
        MEETUP_LIST.append(self.meetup1created)
        response = self.client.get(
            '/api/v1/meetups/1', data=json.dumps(self.meetup1), content_type="application/json")
        meet_got = json.loads(response.data.decode("utf-8", KEY))
        self.assertEqual(meet_got["data"], self.meetup1created)
        self.assertEqual(response.status_code, 200)

    def test_get_single_meetup_fail(self):
        MEETUP_LIST.append(self.meetup1created)
        response = self.client.get(
            '/api/v1/meetups/1000', data=json.dumps(self.meetup1), content_type="application/json")
        self.assertEqual(response.status_code, 404)

    def test_delete_meetup_fail(self):
        response = self.client.delete(
            '/api/v1/meetups/1000', data=json.dumps(self.meetup1), content_type="application/json")
        delete_fail_resp = json.loads(response.data.decode("utf-8", KEY))
        self.assertEqual(delete_fail_resp["error"], "meetup was not found")
        self.assertEqual(response.status_code, 404)

    def test_delete_meetup_success(self):
        response = self.client.delete(
            '/api/v1/meetups/1', data=json.dumps(self.meetup1), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_meetup_missing_tag_field(self):
        """ test when meetup has no tags """
        response = self.client.post(
            '/api/v1/meetups', data=json.dumps(self.meetup_no_tags), content_type="application/json")
        resp_details = json.loads(response.data.decode("utf-8", KEY))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(resp_details["error"],
                         "tag field is missing")

    def test_meetup_missing_tags_desc(self):
        """ test when meetup has no tags """
        response = self.client.post(
            '/api/v1/meetups', data=json.dumps(self.meetup_no_tags_details), content_type="application/json")
        resp_details = json.loads(response.data.decode("utf-8", KEY))
        self.assertEqual(response.status_code, 422)
        self.assertEqual(resp_details["error"],
                         "at least 1 tag is required[#name_of_tag]")

    def test_meetup_tag_whitespace(self):
        """ test when meetup has no tags """
        response = self.client.post(
            '/api/v1/meetups', data=json.dumps(self.meetup_whitespace_in_tag), content_type="application/json")
        resp_details = json.loads(response.data.decode("utf-8", KEY))
        self.assertEqual(response.status_code, 422)
        self.assertEqual(resp_details["error"],
                         "tag input cannot be empty whitespace!!")

    def test_meetup_conflict_existing(self):
        """ test when meetup wih similar details exist """
        response = self.client.post(
            '/api/v1/meetups', data=json.dumps(self.meetup1created), content_type="application/json")
        resp_details = json.loads(response.data.decode("utf-8", KEY))
        self.assertEqual(response.status_code, 409)
        self.assertEqual(resp_details["error"],
                         "you may be trying to make a meetup duplicate, please confirm!!")

    def test_missing_topic_field(self):
        """ test when meetup has no topic field """
        response = self.client.post(
            '/api/v1/meetups', data=json.dumps(self.meetup2), content_type="application/json")
        resp_details = json.loads(response.data.decode("utf-8", KEY))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(resp_details["error"],
                         "topic field is missing")

    def test_missing_topic_field_only_whitespace(self):
        """ test when meetup has no topic field """
        response = self.client.post(
            '/api/v1/meetups', data=json.dumps(self.meetup21), content_type="application/json")
        resp_details = json.loads(response.data.decode("utf-8", KEY))
        self.assertEqual(response.status_code, 422)
        self.assertEqual(resp_details["error"],
                         "topic cannot contain whitespace only")

    def test_missing_topic_field_empty(self):
        """ test when meetup has no topic field """
        response = self.client.post(
            '/api/v1/meetups', data=json.dumps(self.meetup211), content_type="application/json")
        resp_details = json.loads(response.data.decode("utf-8", KEY))
        self.assertEqual(response.status_code, 422)
        self.assertEqual(resp_details["error"],
                         "topic cannot be empty!!")
