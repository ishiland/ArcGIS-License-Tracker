from flask_testing import TestCase

from app import app, db


class BaseTestCase(TestCase):
    def create_app(self):
        app.config.from_object('app.config.TestingConfig')
        return app

    def setUp(self):
        db.create_all(bind=None)
        db.session.commit()

        with open('tests/data.txt') as data:
            self.lines = data.read()

    def tearDown(self):
        db.session.remove()
        db.drop_all(bind=None)