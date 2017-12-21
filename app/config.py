import logging

TIMEZONE = 'US/Eastern'

# Secret key for generating tokens
SECRET_KEY = 'houdini'

# Database choice
SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

DEBUG = False

LOG_LEVEL = logging.DEBUG
LOG_FILENAME = 'activity.log'

LOG_MAXBYTES = 20000
LOG_BACKUPS = 0
