import unittest
from flask_script import Manager, Shell, Server
from app import app, db

manager = Manager(app)

def make_shell_context():
    return dict(app=app)

@manager.command
def recreate_db():
    """
    Create the SQL database.
    """
    db.drop_all()
    db.create_all()
    db.session.commit()
    print("recreated the database")

@manager.command
def test():
    """
    run unit tests
    :return: result, successful or not
    """
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

@manager.command
def read_once():
    """
    a one-time read from the license server.
    """
    from app.read_licenses import read
    read()
    print('Read completed. Check logs for errors. ')


manager.add_command('runserver', Server(threaded=True))
manager.add_command('shell', Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()
