import os
from flask import Flask

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


if flask_env != 'development':
    """
    Create a scheduler to update license data in background. 
    Only run this in production since the development reloader will duplicate background tasks.
    """
    from app.read_licenses import read
    from app.arcgis_config import UPDATE_INTERVAL
    from apscheduler.schedulers.background import BackgroundScheduler
    import atexit
    scheduler = BackgroundScheduler()
    scheduler.add_job(read, trigger='interval', minutes=UPDATE_INTERVAL, max_instances=1)
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown(wait=False))

# Import the views
from app.views import main, error
