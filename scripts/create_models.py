import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from models import *
from scripts.stored_procs import mssql


def create():
    # create tables
    Base.metadata.create_all(engine)

    # create stored procedures
    for m in mssql:
        engine.execute(m)

if __name__ == '__main__':
    create()