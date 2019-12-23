from flask import Flask

app = Flask(__name__)

# Setup the app with the config.py file
app.config.from_object('app.config.DevelopmentConfig')

# Setup the logger
# from app.logger_setup import logger

# Setup the database
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

# Setup the debug toolbar
from flask_debugtoolbar import DebugToolbarExtension
toolbar = DebugToolbarExtension(app)

# Create a scheduler to update license data in background
# from app.read_licenses import read
# from app.arcgis_config import UPDATE_INTERVAL
# from apscheduler.schedulers.background import BackgroundScheduler
# import atexit
# scheduler = BackgroundScheduler()
# scheduler.add_job(read, trigger='interval', minutes=UPDATE_INTERVAL, max_instances=1)
# scheduler.start()
# atexit.register(lambda: scheduler.shutdown(wait=False))

# Import the views
from app.views import main, error

