""" API config File """
import os
db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")


class Config(object):
    """ Parent configuration class """
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv("SECRET")


class DevelopmentConfig(Config):
    """ Configuration for development environment """
    DEBUG = True


class StagingConfig(Config):
    """ Configuration for the staging environment """
    DEBUG = True


class TestingConfig(Config):
    """ Configuration for the testing environment """
    TESTING = True
    DB_TEST = os.getenv("DB_URL_TEST")


class ProductionConfig(Config):
    """ Configuration for the production environment """
    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'debug': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig
}
