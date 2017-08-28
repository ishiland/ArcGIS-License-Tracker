# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#
from flask import Flask, render_template, url_for, request, jsonify
import logging
from logging import Formatter, FileHandler
import os
from models import *
from flask_sqlalchemy import SQLAlchemy


# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)

app.config.from_object('config')

db = SQLAlchemy(app)


@app.teardown_request
def shutdown_session(exception=None):
    db.session.remove()


@app.template_filter('trim')
def trim(s):
    return s.strip()


@app.template_filter('relative_time')
def relative_time(t):
    if t:
        t_delta = datetime.now() - t
        t = str(t_delta).split(':')
        time_string = ''
        if int(t[0]) > 0:
            time_string += t[0].lstrip("0") + 'h, '
        if int(t[1]) > 0:
            time_string += t[1].lstrip("0") + 'm '
        if float(t[2]) > 0:
            time_string += t[2].split('.')[0].lstrip("0") + 's'
        return time_string
    else:
        return None


@app.context_processor
def utility_processor():
    def pluralize(i, s):
        if i != 1:
            return s + 's'
        else:
            return s
    return dict(pluralize=pluralize)


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

@app.route('/')
def dashboard():
    servers = db.session.query(Server).all()
    user_count = db.session.query(User).count()
    active_user_count = db.session.query(History.user_id).filter(History.time_in == None).group_by(History.user_id).count()
    workstation_count = db.session.query(Workstation).count()
    return render_template('pages/placeholder.dashboard.html',
                           servers=servers,
                           active_user_count=active_user_count,
                           workstation_count=workstation_count,
                           user_count=user_count)


@app.route('/_data/server/availability')
def server_availability():
    servername = request.args.get('servername')
    ext = request.args.get('ext')
    availability = db.session.execute("flexlm_product_availability :p1,:p2", {'p1':'core', 'p2': servername}).fetchall()
    # availability = db.session.query(Product).filter(Product.type == 'core').join(Server).filter(Server.name == servername).all()
    if ext:
        extensions = db.session.execute("flexlm_product_availability :p1,:p2", {'p1': 'extension', 'p2': servername}).fetchall()
        return jsonify(core=[[x for x in a] for a in availability], ext=[[x for x in e] for e in extensions])
    else:
        return jsonify(core=[[x for x in a] for a in availability])


@app.route('/_data/product/availability')
def product_availability():
    servername = request.args.get('servername')
    product = request.args.get('product')
    availability = db.session.execute("flexlm_active_users_by_product :p1,:p2", {'p1': product, 'p2': servername}).fetchall()
    return jsonify([[x for x in a] for a in availability])


@app.route('/products')
def products():
    servers = db.session.query(Server).all()
    server = request.args.get('server')
    core_products = db.session.execute("flexlm_products_by_server :p1,:p2", {'p1': 'core', 'p2': server}).fetchall()
    ext_products = db.session.execute("flexlm_products_by_server :p1,:p2", {'p1': 'extension', 'p2': server}).fetchall()
    return render_template('pages/placeholder.products.html',
                           servers=servers,
                           core=core_products,
                           ext=ext_products)


@app.route('/products/<servername>/<productname>')
def productname(servername, productname, days=7):
    chart_data = db.session.execute("flexlm_product_chartdata :p1,:p2,:p3", {'p1': productname, 'p2': servername, 'p3': days}).fetchall()
    usage = db.session.execute("flexlm_product_usage_details :p1,:p2", {'p1': productname, 'p2': servername}).fetchall()
    workstations = db.session.execute("flexlm_product_workstation :p1,:p2", {'p1': productname, 'p2': servername}).fetchall()
    info = db.session.execute("flexlm_product_status :p1,:p2", {'p1': productname, 'p2': servername}).fetchall()
    return render_template('pages/placeholder.productname.html',
                           chart_data=chart_data,
                           info=info[0],
                           usage=usage,
                           ws=workstations)


@app.route('/users')
def users():
    users = db.session.execute("EXEC flexlm_all_users")
    return render_template('pages/placeholder.users.html',
                           users=users)


@app.route('/users/<username>')
def username(username):
    workstations = db.session.execute("flexlm_user_workstation :p1", {'p1': username}).fetchall()
    product_usage = db.session.execute("flexlm_user_usage_details :p1", {'p1': username}).fetchall()
    license_server_usage = db.session.execute("flexlm_user_server :p1", {'p1': username}).fetchall()
    return render_template('pages/placeholder.username.html',
                           workstations=workstations,
                           license_server_usage=license_server_usage,
                           product_usage=product_usage)


@app.route('/servers')
def servers():
    servers = db.session.execute("EXEC flexlm_servers_all")
    return render_template('pages/placeholder.servers.html',
                           servers=servers)


@app.route('/servers/<servername>')
def servername(servername):
    server_status = db.session.execute("flexlm_server_status :p1", {'p1': servername}).fetchall()
    server_history = db.session.execute("flexlm_server_history :p1", {'p1': servername}).fetchall()
    user_count = db.session.execute("flexlm_server_unique_users :p1", {'p1': servername}).fetchall()
    products = db.session.execute("flexlm_server_products :p1", {'p1': servername}).fetchall()
    start_date = db.session.execute("flexlm_server_startdate :p1", {'p1': servername}).fetchall()
    return render_template('pages/placeholder.servername.html',
                           server_status=server_status[0],
                           server_history=server_history,
                           user_count=user_count[0][0],
                           products=products,
                           start_date=start_date[0][0])


@app.route('/workstations')
def workstations():
    ws = db.session.execute("flexlm_all_workstations")
    return render_template('pages/placeholder.workstations.html',
                           ws=ws)


@app.route('/workstations/<workstationname>')
def workstationname(workstationname):
    users = db.session.execute("flexlm_ws_user :p1", {'p1': workstationname}).fetchall()
    product_usage = db.session.execute("flexlm_ws_usage_details :p1", {'p1': workstationname}).fetchall()
    license_server_usage = db.session.execute("flexlm_ws_server :p1", {'p1': workstationname}).fetchall()
    return render_template('pages/placeholder.workstationname.html',
                           users=users,
                           license_server_usage=license_server_usage,
                           product_usage=product_usage)

# Error handlers.
@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
# if __name__ == '__main__':
#     app.run()

# Or specify port manually:
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
