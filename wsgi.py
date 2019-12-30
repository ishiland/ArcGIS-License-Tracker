# python 3
# used for wsgi apache deployment
import os, sys
PROJECT_DIR = os.path.dirname(os.path.realpath(__file__))
activate_this = os.path.join(PROJECT_DIR, 'venv', 'Scripts', 'activate_this.py')
with open(activate_this) as file_:
   exec(file_.read(), dict(__file__=activate_this))
sys.path.append(PROJECT_DIR)
from app import app as application