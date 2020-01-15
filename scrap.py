from app import db
from app.models import User, Workstation, Product, History, Server, Updates



sname = 'gv-gislicense'
pname = 'ARC/INFO'
# active = db.session.query(User.name, Workstation.name, Product.common_name,
#                           History.time_in, History.time_out, Server.name). \
#     filter(User.id == History.user_id). \
#     filter(Product.id == History.product_id). \
#     filter(Workstation.id == History.workstation_id). \
#     filter(Server.id == Product.server_id). \
#     filter(Product.internal_name == pname). \
#     filter(Server.name == sname). \
#     filter(History.time_in == None).all()
#
#
# results = db.session.query(History.time_in, Workstation.name, User.name, Product.common_name, Server.name).filter(
#     User.id == History.user_id, Product.id == History.product_id, Workstation.id == History.workstation_id,
#     Server.id == Product.server_id, History.update_id == Updates.id, History.time_in == None).all()

results = db.session.query(History.time_in, Workstation.name, User.name, Product.common_name, Server.name). \
    filter(User.id == History.user_id). \
    filter(Server.id == Product.server_id). \
    filter(Workstation.id == History.workstation_id). \
    filter(History.update_id == Updates.id). \
    filter(History.time_in == None).all()

for r in results:
    print(r)
