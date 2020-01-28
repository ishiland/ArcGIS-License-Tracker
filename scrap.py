from app import db
from app.models import User, Workstation, Product, History, Server, Updates
from pprint import pprint

sname = 'gv-gislicense'
pname = 'ARC/INFO'


def serialize_dashboard_data(data):
    """serializes current license data for the dashboard"""
    obj = {}
    for d in data:
        if d[5] not in obj:
            obj[d[5]] = {d[2]: {'users': [],
                                'active': d[3],
                                'total': d[4]}}
            if d[6] is None:
                obj[d[5]][d[2]]['users'].append({'workstation': d[0], 'username': d[1]})

        else:
            if d[2] not in obj[d[5]]:
                obj[d[5]][d[2]] = {'users': [],
                                   'active': d[3],
                                   'total': d[4]}
            if d[6] is None:
                obj[d[5]][d[2]]['users'].append({'workstation': d[0], 'username': d[1]})
    return obj


# active = db.session.query(Workstation.name, User.name, Product.common_name, Product.license_out,
#                           Product.license_total, Server.name, History.time_in). \
#     filter(History.user_id == User.id,
#            History.update_id == Updates.id,
#            History.workstation_id == Workstation.id,
#            Product.server_id == Server.id,
#            History.product_id == Product.id).all()
#
# for a in active:
#     print(a)

import random
from datetime import timedelta, datetime


def random_date():
    """
    This function will return a random datetime between two datetime
    objects.
    """
    start_date = datetime.now() + timedelta(-15)
    start = datetime.strptime(start_date.strftime('%Y-%m-%d %I:%M:%S'), '%Y-%m-%d %I:%M:%S')
    end = datetime.strptime(datetime.now().strftime('%Y-%m-%d %I:%M:%S'), '%Y-%m-%d %I:%M:%S')
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)


for x in range(100):
    r = random_date()

    print(r)
