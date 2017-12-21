from flask import Flask

app = Flask(__name__)

# Setup the app with the config.py file
app.config.from_object('app.config')

# Setup the logger
from app.logger_setup import logger

# Setup the database
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

# Setup the debug toolbar
from flask_debugtoolbar import DebugToolbarExtension
app.config['DEBUG_TB_TEMPLATE_EDITOR_ENABLED'] = True
app.config['DEBUG_TB_PROFILER_ENABLED'] = True
toolbar = DebugToolbarExtension(app)

# Create a scheduler to update license data in background
from app.toolbox import lm_read, lm_config
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
scheduler = BackgroundScheduler()
scheduler.add_job(lm_read.run, trigger='interval', minutes=lm_config.UPDATE_INTERVAL, max_instances=1)
scheduler.start()
atexit.register(lambda: scheduler.shutdown(wait=False))

# Import the views
from app.views import main, error

