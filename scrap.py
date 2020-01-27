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


all_products = db.session.query(Product.common_name, Product.license_out, Product.license_total, Server.name).filter(Product.server_id==Server.id).all()

for a in all_products:
    print(dir(a))


