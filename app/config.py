import logging


class BaseConfig(object):
    """Base configuration"""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG_TB_ENABLED = False
    # DEBUG_TB_INTERCEPT_REDIRECTS = False
    TIMEZONE = 'US/Eastern'
    LOG_LEVEL = logging.DEBUG
    LOG_FILENAME = 'activity.log'
    LOG_MAXBYTES = 20000
    LOG_BACKUPS = 0
    SECRET_KEY ='houdini'


class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app_dev.db'
    """Development configuration"""
    # DEBUG_TB_TEMPLATE_EDITOR_ENABLED = True
    DEBUG_TB_ENABLED = True
    DEBUG = True


class TestingConfig(BaseConfig):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app_test.db'


class ProductionConfig(BaseConfig):
    """Testing configuration"""
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'