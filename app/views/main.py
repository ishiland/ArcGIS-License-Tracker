from flask import render_template, jsonify, request
from sqlalchemy import desc, asc, func, extract, and_
from app import app, models, db
import json
import datetime
import humanize


@app.route('/')
@app.route('/index')
@app.route('/dashboard')
def dashboard():
    servers = db.session.query(models.Server).all()
    user_count = db.session.query(models.User).count()
    active_users = db.session.query(models.User).join(models.History).filter(models.History.time_in == None).join(
        models.Product).filter(
        models.Product.type == 'core').all()
    workstation_count = db.session.query(models.Workstation).count()
    return render_template('index.html',
                           servers=servers,
                           active_users=active_users,
                           workstation_count=workstation_count,
                           user_count=user_count)


@app.route('/data/server/availability')
def server_availability():
    """
    Gets the core and extension product availability on a license server.
    :return: Availability of products on a license server.
    """
    s = request.args.get('servername')
    core = db.session.query(models.Product, models.Server).filter(models.Product.type == 'core'). \
        filter(models.Product.server_id == models.Server.id).filter(models.Server.name == s).all()
    ext = db.session.query(models.Product, models.Server).filter(models.Product.type == 'extension'). \
        filter(models.Product.server_id == models.Server.id).filter(models.Server.name == s).all()
    return json.dumps(core + ext, cls=models.AlchemyEncoder)


@app.route('/data/product/availability')
def product_availability():
    """

    :return: Active users by product name
    """
    sname = request.args.get('servername')
    pname = request.args.get('product')
    active = db.session.query(models.User.name, models.Workstation.name, models.Product.common_name,
                              models.History.time_in, models.History.time_out, models.Server.name). \
        filter(models.User.id == models.History.user_id). \
        filter(models.Product.id == models.History.product_id). \
        filter(models.Workstation.id == models.History.workstation_id). \
        filter(models.Server.id == models.Product.server_id). \
        filter(models.Product.common_name == pname). \
        filter(models.Server.name == sname). \
        filter(models.History.time_in == None).all()
    return jsonify(results=[[x for x in a] for a in active])


@app.route('/data/active_users')
def active_users():
    active = db.session.query(models.User).join(models.History).filter(models.History.time_in == None).join(
        models.Product).filter(
        models.Product.type == 'core').all()
    return active


@app.route('/products/<servername>/<productname>')
def productname(servername, productname, days=3):
    users = db.session.query(models.User.name, models.History.time_in,
                             func.sum(func.julianday(func.ifnull(models.History.calculated_timein,
                                                                 datetime.datetime.now())) - func.julianday(
                                 models.History.time_out)).label('time_sum')). \
        filter(models.User.id == models.History.user_id). \
        filter(models.History.product_id == models.Product.id). \
        filter(models.Product.common_name == productname). \
        distinct(models.User.name).group_by(models.User.name).all()

    days = datetime.datetime.utcnow() - datetime.timedelta(days=days)

    chart_data = db.session.query(func.count(models.History.user_id).label('users'), models.Product.license_total,
                                  extract('month', models.History.time_out).label('m'),
                                  extract('day', models.History.time_out).label('d'),
                                  extract('year', models.History.time_out).label('y')). \
        filter(models.Product.id == models.History.product_id). \
        filter(models.Server.id == models.Updates.server_id). \
        filter(models.Updates.id == models.History.update_id). \
        filter(models.Server.name == servername). \
        filter(models.History.time_out > days). \
        filter(models.Product.common_name == productname). \
        distinct(models.History.user_id). \
        group_by(models.Product.common_name, models.Server.name, 'm', 'd', 'y'). \
        order_by(desc('y')).order_by(desc('m')).order_by(desc('d')).all()

    info = db.session.query(models.Product). \
        filter(models.Server.id == models.Product.server_id). \
        filter(models.Server.name == servername). \
        filter(models.Product.common_name == productname).first()
    return render_template('pages/productname.html',
                           users=users,
                           chart_data=chart_data,
                           info=info)


@app.route('/_productchart')
def productchart():
    selection = request.args.get('days')
    servername = request.args.get('servername')
    productname = request.args.get('productname')
    days = datetime.datetime.utcnow() - datetime.timedelta(days=int(selection))
    chart_data = db.session.query(func.count(models.History.user_id).label('users'), models.Product.license_total,
                                  extract('month', models.History.time_out).label('m'),
                                  extract('day', models.History.time_out).label('d'),
                                  extract('year', models.History.time_out).label('y')). \
        filter(models.Product.id == models.History.product_id). \
        filter(models.Server.id == models.Updates.server_id). \
        filter(models.Updates.id == models.History.update_id). \
        filter(models.Server.name == servername). \
        filter(models.History.time_out > days). \
        filter(models.Product.common_name == productname). \
        distinct(models.History.user_id). \
        group_by(models.Product.common_name, models.Server.name, 'm', 'd', 'y'). \
        order_by(desc('y')).order_by(desc('m')).order_by(desc('d')).all()
    return jsonify(result=chart_data)


@app.route('/users')
def users():
    all_users = db.session.query(models.User.name, models.History.time_in,
                                 func.sum(func.julianday(func.ifnull(models.History.calculated_timein,
                                                                     datetime.datetime.now())) - func.julianday(
                                     models.History.time_out)).label('time_sum')). \
        filter(models.User.id == models.History.user_id). \
        filter(models.History.product_id == models.Product.id). \
        filter(models.Product.type == 'core'). \
        distinct(models.User.name).group_by(models.User.name).all()
    return render_template('pages/users.html',
                           users=all_users)


@app.route('/users/<username>')
def username(username):
    workstations = db.session.query(models.Workstation, models.History). \
        filter(models.User.id == models.History.user_id). \
        filter(models.Workstation.id == models.History.workstation_id). \
        group_by(models.Workstation.name).distinct(models.Workstation.name). \
        filter(models.User.name == username).all()

    servers = db.session.query(models.Server, models.History). \
        filter(models.User.id == models.History.user_id). \
        filter(models.Updates.id == models.History.update_id). \
        filter(models.Server.id == models.Updates.server_id). \
        filter(models.User.name == username). \
        group_by(models.Server.name).distinct(models.Server.name).all()

    products = db.session.query(models.Product.common_name, models.Product.type, models.History.time_in,
                                func.sum(func.julianday(func.ifnull(models.History.calculated_timein,
                                                                    datetime.datetime.now())) - func.julianday(
                                    models.History.time_out)).label('time_sum')). \
        filter(models.User.id == models.History.user_id). \
        filter(models.User.name == username). \
        filter(models.History.product_id == models.Product.id). \
        group_by(models.Product.common_name).distinct(models.Product.common_name).all()
    return render_template('pages/username.html',
                           workstations=workstations,
                           servers=servers,
                           products=products)


@app.route('/servers')
def servers():
    subq = db.session.query(
        models.Server.name,
        func.max(models.Updates.time_complete).label('maxdate')
    ).filter(models.Server.id == models.Updates.server_id).group_by(models.Server.name).subquery('t2')

    query = db.session.query(models.Updates, models.Server).join(
        subq,
        and_(
            models.Server.name == subq.c.name,
            models.Updates.time_complete == subq.c.maxdate
        )
    )

    return render_template('pages/servers.html', servers=query)


@app.route('/servers/<servername>')
def servername(servername):
    status = db.session.query(models.Server, models.Updates). \
        filter(models.Server.id == models.Updates.server_id). \
        filter(models.Server.name == servername). \
        order_by(desc(models.Updates.time_start)).limit(1).first()
    history = db.session.query(models.Server, models.Updates). \
        filter(models.Server.id == models.Updates.server_id). \
        filter(models.Server.name == servername). \
        filter(models.Updates.status != 'OK'). \
        order_by(desc(models.Updates.time_start)).all()
    users = db.session.query(models.User, models.History, models.Server, models.Updates, models.Product). \
        filter(models.User.id == models.History.user_id). \
        filter(models.Updates.id == models.History.update_id). \
        filter(models.Product.id == models.History.product_id). \
        filter(models.Server.id == models.Updates.server_id). \
        filter(models.Product.type == 'core'). \
        filter(models.Server.name == servername). \
        distinct(models.User.name).group_by(models.User.name).all()
    first_update = db.session.query(models.Updates). \
        filter(models.Server.id == models.Updates.server_id). \
        filter(models.Server.name == servername). \
        order_by(asc(models.Updates.time_start)).limit(1).first()
    return render_template('pages/servername.html',
                           chart_data=None,
                           status=status,
                           history=history,
                           users=users,
                           start_date=first_update)


@app.route('/workstations')
def workstations():
    all_ws = db.session.query(models.Workstation.name, models.History.time_in,
                              func.sum(func.julianday(func.ifnull(models.History.calculated_timein,
                                                                  datetime.datetime.now())) - func.julianday(
                                  models.History.time_out)).label('time_sum')). \
        filter(models.Workstation.id == models.History.workstation_id). \
        filter(models.History.product_id == models.Product.id). \
        filter(models.Product.type == 'core'). \
        distinct(models.Workstation.name).group_by(models.Workstation.name).all()
    return render_template('pages/workstations.html',
                           ws=all_ws)


@app.route('/workstations/<workstationname>')
def workstationname(workstationname):
    users = db.session.query(models.User.name, models.History.time_in). \
        filter(models.User.id == models.History.user_id). \
        filter(models.Workstation.id == models.History.workstation_id). \
        group_by(models.User.name).distinct(models.User.name). \
        filter(models.Workstation.name == workstationname).all()

    servers = db.session.query(models.Server, models.History.time_in). \
        filter(models.Workstation.id == models.History.workstation_id). \
        filter(models.Updates.id == models.History.update_id). \
        filter(models.Server.id == models.Updates.server_id). \
        filter(models.Workstation.name == workstationname). \
        group_by(models.Server.name).distinct(models.Server.name).all()

    products = db.session.query(models.Product.common_name, models.Product.type, models.History.time_in,
                                func.sum(func.julianday(func.ifnull(models.History.calculated_timein,
                                                                    datetime.datetime.now())) - func.julianday(
                                    models.History.time_out)).label('time_sum')). \
        filter(models.Workstation.id == models.History.workstation_id). \
        filter(models.Workstation.name == workstationname). \
        filter(models.History.product_id == models.Product.id). \
        group_by(models.Product.common_name).distinct(models.Product.common_name).all()
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
