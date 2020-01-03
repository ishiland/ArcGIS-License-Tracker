from flask_testing import TestCase
import os
from app import app, db

dir_path = os.path.dirname(os.path.realpath(__file__))

class BaseTestCase(TestCase):
    def create_app(self):
        app.config.from_object('app.config.TestingConfig')
        return app

    def setUp(self):
        db.create_all(bind=None)
        db.session.commit()

        with open(os.path.join(dir_path, 'data.txt')) as data:
            self.lines = data.read()

    def tearDown(self):
        db.session.remove()
        db.drop_all(bind=None)