from flask_script import Manager, prompt_bool, Shell, Server
from termcolor import colored
import colorama
from app import app, db

colorama.init()

manager = Manager(app)


def make_shell_context():
    return dict(app=app)


@manager.command
def initdb():
    ''' Create the SQL database. '''
    db.create_all()
    print(colored('The SQL database has been created', 'green'))


@manager.command
def dropdb():
    ''' Delete the SQL database. '''
    if prompt_bool('Are you sure you want to lose all your SQL data?'):
        db.drop_all()
        print(colored('The SQL database has been deleted', 'green'))


@manager.command
def read():
    from app.toolbox.lm_read import run
    ''' Read data from the license server. '''
    read_data = run()
    if not read_data:
        print(colored('Read completed successfully.', 'green'))
    else:
        print(colored('There was a problem reading from your license server.', 'red'))


# Set the use_reloader to False so the `lm_read.py` process is not duplicated
manager.add_command('runserver', Server(use_reloader=False))
manager.add_command('shell', Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()
