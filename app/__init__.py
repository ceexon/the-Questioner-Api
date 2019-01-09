from flask import Flask, Blueprint
from instanse.config import app_config
from app.api.v1.views.user_views import v1_mod


def my_app(config_name):
    app = Flask(__name__)

    app.config.from_object(app_config[config_name])

    app.register_blueprint(v1_mod, url_prefix="/api/v1")

    return app
