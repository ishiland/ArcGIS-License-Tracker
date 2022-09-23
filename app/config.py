import logging
import os


class BaseConfig(object):
    """Base configuration"""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG_TB_ENABLED = False
    TIMEZONE = 'US/Eastern'
    LOG_LEVEL = logging.INFO
    LOG_FILENAME = 'activity.log'
    LOG_MAXBYTES = 20000
    LOG_BACKUPS = 0
    SECRET_KEY = 'houdini'
    # use sqlite by default
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'


class DevelopmentConfig(BaseConfig):
    DEBUG_TB_ENABLED = True
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(BaseConfig):
    # use sqlite by default
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    TESTING = True


class ProductionConfig(BaseConfig):
    DEBUG = False
