from flask import Blueprint, request, jsonify
import datetime
from app.api.v1.models.models import Users
from user_views import v1_mod

time_now = datetime.datetime.now()


@v1_mod.route('/meetu[', methods=['POST'])
def create_meetup():
    pass
