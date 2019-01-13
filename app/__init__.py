import os
from flask import Flask, Blueprint
from instanse.config import app_config
from app.api.v1.views.user_views import V1_MOD
from app.api.v1.views.meet_views import V1_MOD
from app.api.v1.views.question_views import V1_MOD


def create_app(name_conf):
    my_app = Flask(__name__)
    # my_app.config.from_object(app_config["development"])
    my_app.config['SECRET_KEY'] = os.getenv("SECRET")
    my_app.register_blueprint(V1_MOD, url_prefix="/api/v1")

    return my_app
