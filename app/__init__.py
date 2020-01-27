import os
from flask import Flask
from flask_apscheduler import APScheduler
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

flask_env = os.environ.get('FLASK_ENV')

if flask_env == 'production':
    print("Using Production configuration")
    app.config.from_object('app.config.ProductionConfig')
else:
    app.config.from_object('app.config.DevelopmentConfig')
    # Setup the debug toolbar
    from flask_debugtoolbar import DebugToolbarExtension
    toolbar = DebugToolbarExtension(app)

# Setup the database
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

# scheduler = APScheduler(BackgroundScheduler())
# scheduler.init_app(app)

# Import the views
from app.views import main, error
