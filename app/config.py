import logging
import os
from app.arcgis_config import UPDATE_INTERVAL

SCHEDULER_JOBS = [
    {
        'id': 'read',
        'func': 'app.read_licenses:read',
        'trigger': 'interval',
        'minutes': UPDATE_INTERVAL
    }
]


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
    SECRET_KEY ='houdini'
    JOBS = SCHEDULER_JOBS
    SCHEDULER_JOB_DEFAULTS = {
        'coalesce': False,
        'max_instances': 1
    }
    # use sqlite by default
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///app.db')


class DevelopmentConfig(BaseConfig):
    DEBUG_TB_ENABLED = True
    DEVELOPMENT = True
    DEBUG = True
    SCHEDULER_API_ENABLED = False


class TestingConfig(BaseConfig):
    # use sqlite by default
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    TESTING = True
    SCHEDULER_API_ENABLED = False


class ProductionConfig(BaseConfig):
    DEBUG = False
    SCHEDULER_API_ENABLED = True
