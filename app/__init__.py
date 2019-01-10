from flask import Flask, Blueprint
from instanse.config import app_config
from app.api.v1.views.user_views import v1_mod
from app.api.v1.views.meet_views import v1_mod

my_app = Flask(__name__)
# my_app.config.from_object(app_config["development"])
my_app.config['SECRET_KEY'] = "uudye78tgde6refs55w7iwtsj"
my_app.register_blueprint(v1_mod, url_prefix="/api/v1")
