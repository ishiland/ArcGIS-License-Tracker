from flask import render_template, make_response, jsonify, request
from sqlalchemy import desc, asc, func, extract, and_
from app import app, db
from app.models import User, Product, Server, Updates, History, Workstation, AlchemyEncoder
import json
import datetime
import humanize


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

@app.route('/dashboard')
@app.route('/')
def dashboard():
    server_count = db.session.query(Server).count()
    user_count = db.session.query(User).count()
    product_count = db.session.query(Product).count()
    workstation_count = db.session.query(Workstation).count()
    active_user_count = db.session.query(User).join(History).filter(History.time_in == None).join(
        Product).filter( Product.type == 'core').count()

    active = db.session.query(Workstation.name, User.name, Product.common_name, Product.license_out,
                              Product.license_total, Server.name, History.time_in). \
        filter(History.user_id == User.id,
               History.update_id == Updates.id,
               History.workstation_id == Workstation.id,
               Product.server_id == Server.id,
               History.product_id == Product.id).all()

    detail = serialize_dashboard_data(active)
    return render_template('index.html',
                           server_count=server_count,
                           user_count=user_count,
                           active_user_count=active_user_count,
                           product_count=product_count,
                           workstation_count=workstation_count,
                           detail=detail)

@app.route('/data/server/availability')
def server_availability():
    """
    Gets the core and extension product availability on a license server.
    :return: Availability of products on a license server.
    """
    s = request.args.get('servername')
    core = db.session.query(Product, Server).filter(Product.type == 'core'). \
        filter(Product.server_id == Server.id).filter(Server.name == s).all()
    ext = db.session.query(Product, Server).filter(Product.type == 'extension'). \
        filter(Product.server_id == Server.id).filter(Server.name == s).all()
    return json.dumps(core + ext, cls=AlchemyEncoder)


@app.route('/data/product/availability')
def product_availability():
    """

    :return: Active users by product name
    """
    sname = request.args.get('servername')
    pname = request.args.get('product')
    active = db.session.query(User.name, Workstation.name, Product.common_name,
                              History.time_in, History.time_out, Server.name). \
        filter(User.id == History.user_id). \
        filter(Product.id == History.product_id). \
        filter(Workstation.id == History.workstation_id). \
        filter(Server.id == Product.server_id). \
        filter(Product.internal_name == pname). \
        filter(Server.name == sname). \
        filter(History.time_in == None).all()
    return jsonify(results=[[x for x in a] for a in active])


@app.route('/data/active_users')
def active_users():
    active = db.session.query(User).join(History).filter(History.time_in == None).join(
        Product).filter(
        Product.type == 'core').all()
    return active


@app.route('/products')
def products():
    all_products = db.session.query(Product.common_name, Product.license_out, Product.license_total, Server.name).filter(Product.server_id==Server.id).all()
    return render_template('pages/products.html',
                           products=all_products)


@app.route('/products/<product_name>')
def productname(product_name):
    users = db.session.query(User.name, History.time_in,
                             Server.name.label('servername'),
                             func.sum(func.julianday(func.ifnull(History.calculated_timein,
                                                                 datetime.datetime.now())) - func.julianday(
                                 History.time_out)).label('time_sum')). \
        filter(User.id == History.user_id). \
        filter(History.product_id == Product.id). \
        filter(Product.server_id == Server.id). \
        filter(Product.common_name == product_name). \
        distinct(User.name).group_by(User.name).all()

    # days = datetime.datetime.utcnow() - datetime.timedelta(days=days)

    # chart_data = db.session.query(func.count(History.user_id).label('users'), Product.license_total,
    #                               extract('month', History.time_out).label('m'),
    #                               extract('day', History.time_out).label('d'),
    #                               extract('year', History.time_out).label('y')). \
    #     filter(Product.id == History.product_id). \
    #     filter(Server.id == Updates.server_id). \
    #     filter(Updates.id == History.update_id). \
    #     filter(Server.name == server_name). \
    #     filter(Product.common_name == product_name). \
    #     distinct(History.user_id). \
    #     group_by(Product.common_name, Server.name, 'm', 'd', 'y'). \
    #     order_by(desc('y')).order_by(desc('m')).order_by(desc('d')).all()
    #  filter(History.time_out > days).

    # info = db.session.query(Product). \
    #     filter(Server.id == Product.server_id). \
    #     filter(Server.name == server_name). \
    #     filter(Product.common_name == product_name).first()
    return render_template('pages/productname.html',
                           users=users,
                           # chart_data=chart_data,
                           # info=info
                           )


# @app.route('/_productchart')
# def productchart():
#     selection = request.args.get('days')
#     servername = request.args.get('servername')
#     productname = request.args.get('productname')
#     days = datetime.datetime.utcnow() - datetime.timedelta(days=int(selection))
#     chart_data = db.session.query(func.count(History.user_id).label('users'), Product.license_total,
#                                   extract('month', History.time_out).label('m'),
#                                   extract('day', History.time_out).label('d'),
#                                   extract('year', History.time_out).label('y')). \
#         filter(Product.id == History.product_id). \
#         filter(Server.id == Updates.server_id). \
#         filter(Updates.id == History.update_id). \
#         filter(Server.name == servername). \
#         filter(History.time_out > days). \
#         filter(Product.common_name == productname). \
#         distinct(History.user_id). \
#         group_by(Product.common_name, Server.name, 'm', 'd', 'y'). \
#         order_by(desc('y')).order_by(desc('m')).order_by(desc('d')).all()
#     return jsonify(result=chart_data)


@app.route('/users')
def users():
    all_users = db.session.query(User.name, History.time_in,
                                 func.sum(func.julianday(func.ifnull(History.calculated_timein,
                                                                     datetime.datetime.now())) - func.julianday(
                                     History.time_out)).label('time_sum')). \
        filter(User.id == History.user_id). \
        filter(History.product_id == Product.id). \
        filter(Product.type == 'core'). \
        distinct(User.name).group_by(User.name).all()
    return render_template('pages/users.html',
                           users=all_users)


@app.route('/users/<username>')
def username(username):
    workstations = db.session.query(Workstation, History). \
        filter(User.id == History.user_id). \
        filter(Workstation.id == History.workstation_id). \
        group_by(Workstation.name).distinct(Workstation.name). \
        filter(User.name == username).all()

    servers = db.session.query(Server, History). \
        filter(User.id == History.user_id). \
        filter(Updates.id == History.update_id). \
        filter(Server.id == Updates.server_id). \
        filter(User.name == username). \
        group_by(Server.name).distinct(Server.name).all()

    products = db.session.query(Product.common_name, Product.type, History.time_in,
                                func.sum(func.julianday(func.ifnull(History.calculated_timein,
                                                                    datetime.datetime.now())) - func.julianday(
                                    History.time_out)).label('time_sum')). \
        filter(User.id == History.user_id). \
        filter(User.name == username). \
        filter(History.product_id == Product.id). \
        group_by(Product.common_name).distinct(Product.common_name).all()
    return render_template('pages/username.html',
                           workstations=workstations,
                           servers=servers,
                           products=products)


@app.route('/servers')
def servers():
    query = db.session.query(
        Server.name.label("name"),
        Updates.info.label("info"),
        Updates.status.label("status"),
        Server.id == Updates.server_id,
        func.max(Updates.time_complete).label('maxdate')
    ).filter(Server.id == Updates.server_id).group_by(Server.name).all()
    return render_template('pages/servers.html', servers=query)


@app.route('/servers/<servername>')
def servername(servername):
    status = db.session.query(Server, Updates). \
        filter(Server.id == Updates.server_id). \
        filter(Server.name == servername). \
        order_by(desc(Updates.time_start)).limit(1).first()
    history = db.session.query(Server, Updates). \
        filter(Server.id == Updates.server_id). \
        filter(Server.name == servername). \
        filter(Updates.status != 'UP'). \
        order_by(desc(Updates.time_start)).all()
    users = db.session.query(User, History, Server, Updates, Product). \
        filter(User.id == History.user_id). \
        filter(Updates.id == History.update_id). \
        filter(Product.id == History.product_id). \
        filter(Server.id == Updates.server_id). \
        filter(Product.type == 'core'). \
        filter(Server.name == servername). \
        distinct(User.name).group_by(User.name).all()
    first_update = db.session.query(Updates). \
        filter(Server.id == Updates.server_id). \
        filter(Server.name == servername). \
        order_by(asc(Updates.time_start)).limit(1).first()
    return render_template('pages/servername.html',
                           chart_data=None,
                           status=status,
                           history=history,
                           users=users,
                           start_date=first_update)

#TODO: clear log for updates on server
def clear_log(servername):
    try:
        Updates.clear()
        return make_response('ok', 200)
    except Exception as e:
        return make_response(str(e), 500)


@app.route('/workstations')
def workstations():
    all_ws = db.session.query(Workstation.name, History.time_in,
                              func.sum(func.julianday(func.ifnull(History.calculated_timein,
                                                                  datetime.datetime.now())) - func.julianday(
                                  History.time_out)).label('time_sum')). \
        filter(Workstation.id == History.workstation_id). \
        filter(History.product_id == Product.id). \
        filter(Product.type == 'core'). \
        distinct(Workstation.name).group_by(Workstation.name).all()
    return render_template('pages/workstations.html',
                           ws=all_ws)


@app.route('/workstations/<workstationname>')
def workstationname(workstationname):
    users = db.session.query(User.name, History.time_in). \
        filter(User.id == History.user_id). \
        filter(Workstation.id == History.workstation_id). \
        group_by(User.name).distinct(User.name). \
        filter(Workstation.name == workstationname).all()

    servers = db.session.query(Server, History.time_in). \
        filter(Workstation.id == History.workstation_id). \
        filter(Updates.id == History.update_id). \
        filter(Server.id == Updates.server_id). \
        filter(Workstation.name == workstationname). \
        group_by(Server.name).distinct(Server.name).all()

    products = db.session.query(Product.common_name, Product.type, History.time_in,
                                func.sum(func.julianday(func.ifnull(History.calculated_timein,
                                                                    datetime.datetime.now())) - func.julianday(
                                    History.time_out)).label('time_sum')). \
        filter(Workstation.id == History.workstation_id). \
        filter(Workstation.name == workstationname). \
        filter(History.product_id == Product.id). \
        group_by(Product.common_name).distinct(Product.common_name).all()
    return render_template('pages/workstationname.html',
                           users=users,
                           servers=servers,
                           products=products)


@app.context_processor
def utility_processor():
    def pluralize(i, s):
        if i != 1:
            return s + 's'
        else:
            return s

    return dict(pluralize=pluralize)


@app.template_filter('relative_time')
def relative_time(t):
    if t:
        try:
            humanized = humanize.naturaltime(t)
            return humanized
        except ValueError as v:
            print(v)
            return '0s'
    else:
        return None


@app.template_filter('delta_time')
def delta_time(t):
    if t:
        try:
            h = humanize.naturaldelta(datetime.timedelta(days=t))
            return h
        except ValueError as v:
            print(v)
            return '0'
    else:
        return None
