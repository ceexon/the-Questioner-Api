import os
import psycopg2
from flask import Flask, Blueprint, jsonify
from instanse.config import app_config
from .api.v2.models.db_connect import main


def create_app(name_conf):
    my_app = Flask(__name__)
    # my_app.config.from_object(app_config["development"])
    my_app.config['SECRET_KEY'] = os.getenv("SECRET")
    main()

    @my_app.errorhandler(404)
    def page_not_found(error):
        return jsonify({'error': 'Url not found', 'status': 404}), 404

    @my_app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({'error': 'Method not allowed', 'status': 405}), 405

    return my_app
