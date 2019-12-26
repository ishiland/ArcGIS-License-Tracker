import datetime
from app import db
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.declarative import DeclarativeMeta
import json


class Server(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(35), nullable=False, unique=True)
    port = db.Column(db.String(10), nullable=False)

    def __init__(self, name, port):
        self.name = name
        self.port = port

    def __repr__(self):
        return '<Server %r>' % self.name

    @staticmethod
    def upsert(hostname, port):
        p = db.session.query(Server).filter(Server.name == hostname).first()
        if p is None:
            p = Server(name=hostname,
                       port=port)
            db.session.add(p)
        else:
            p.port = port
        db.session.commit()
        return p.id


class Updates(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    server_id = db.Column(db.Integer, db.ForeignKey("server.id"), nullable=False)
    status = db.Column(db.String(8))
    info = db.Column(db.String(255), default=None)
    time_start = db.Column(db.DateTime)
    time_complete = db.Column(db.DateTime, default=None)
    FlexLM_server = db.relationship(u'Server')

    def __init__(self, time_start, server_id, status, info):
        self.time_start = time_start
        self.server_id = server_id
        self.status = status
        self.info = info

    def __repr__(self):
        return '<Updates %r>' % self.id

    @staticmethod
    def start(server_id):
        insert = Updates(server_id=server_id, time_start=datetime.datetime.now(), status='UPDATING', info=None)
        db.session.add(insert)
        db.session.commit()
        return insert.id

    @staticmethod
    def end(update_id, status=None, info=None):
        db.session.query(Updates).filter_by(id=update_id).update({"status": status,
                                                                  "info": info,
                                                                  "time_complete": datetime.datetime.now()},
                                                                 synchronize_session='fetch')
        db.session.commit()
        db.session.close()


class Product(db.Model):
    __table_args__ = (
        db.UniqueConstraint('server_id', 'internal_name', name='UQ_server_internalname'),
        db.UniqueConstraint('server_id', 'common_name', name='UQ_server_commonname'),
    )
    id = db.Column(db.Integer, primary_key=True)
    server_id = db.Column(db.Integer, db.ForeignKey("server.id"), nullable=False)
    internal_name = db.Column(db.String(35), nullable=False)
    common_name = db.Column(db.String(35), nullable=False)
    category = db.Column(db.String(35), nullable=False)
    type = db.Column(db.String(10), nullable=False)
    expires = db.Column(db.String(50))
    version = db.Column(db.String(5))
    license_out = db.Column(db.Integer)
    license_total = db.Column(db.Integer)
    FlexLM_server = db.relationship(u'Server')

    def __repr__(self):
        return '<Product %r>' % self.common_name

    @staticmethod
    def reset(server_id):
        db.session.query(Product).filter_by(server_id=server_id).update({"license_out": 0})
        db.session.flush()

    @staticmethod
    def upsert(server_id, internal_name, **kwargs):
        p = db.session.query(Product).filter_by(internal_name=internal_name, server_id=server_id)
        if not p.first():
            p = Product(server_id=server_id,
                        internal_name=internal_name,
                        **kwargs)
            db.session.add(p)
            db.session.commit()
            return p.id
        else:
            p.update(kwargs)
            return p.first().id

    @staticmethod
    def query(internal_name, server_id):
        p = db.session.query(Product).filter_by(internal_name=internal_name, server_id=server_id).first()
        return p.id


class Workstation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Workstation %r>' % self.name

    @staticmethod
    def add(workstation):
        w = db.session.query(Workstation).filter_by(name=workstation).first()
        if w is None:
            w = Workstation(name=workstation)
            db.session.add(w)
            db.session.commit()
            return db.session.query(Workstation).filter_by(name=workstation).first().id
        return w.id


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<User %r>' % self.name

    @staticmethod
    def add(username):
        u = db.session.query(User).filter_by(name=username).first()
        if u is None:
            u = User(name=username)
            db.session.add(u)
            db.session.commit()
        return u.id

    @staticmethod
    def delete(name):
        User.query.filter_by(name=name).delete()
        db.session.commit()

    @staticmethod
    def distinct_users():
        return db.session.query(User.name).distinct().all()


class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    workstation_id = db.Column(db.Integer, db.ForeignKey("workstation.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    update_id = db.Column(db.Integer, db.ForeignKey("updates.id"), nullable=False)
    time_out = db.Column(db.DateTime, nullable=False)
    time_in = db.Column(db.DateTime, nullable=True)
    FlexLM_product = db.relationship(u'Product')
    FlexLM_update = db.relationship(u'Updates')
    FlexLM_user = db.relationship(u'User')
    FlexLM_workstation = db.relationship(u'Workstation')

    # def __init__(self, user_id, workstation_id, product_id, update_id, time_out, time_in):
    #     self.user_id = user_id
    #     self.workstation_id = workstation_id
    #     self.product_id = product_id
    #     self.update_id = update_id
    #     self.time_out = time_out
    #     self.time_in = time_in

    def __repr__(self):
        return '<History %r>' % self.id

    @hybrid_property
    def calculated_timein(self):
        if self.time_in:
            return self.time_in
        else:
            return datetime.datetime.now()

    @staticmethod
    # def add(user_id, workstation_id, server_id, product_id, update_id, time_out):
    def add(update_id, server_id, **kwargs):

        h = db.session.query(History).filter_by(user_id=kwargs.get('user_id'),
                                                workstation_id=kwargs.get('workstation_id'),
                                                product_id=kwargs.get('product_id'),
                                                time_in=None).join(Product).filter_by(server_id=server_id).first()
        if h is None:
            h = History(update_id=update_id,
                        time_in=None,
                        **kwargs)
            db.session.add(h)
            db.session.commit()
        return h.id

    @staticmethod
    def time_in_none(server_id):
        t = db.session.query(History).filter_by(time_in=None).join(Product).filter_by(server_id=server_id).all()
        return t

    @staticmethod
    def update(history_id, dt, server_id):
        return db.session.query(History).filter(History.FlexLM_product.has(server_id=server_id),
                                                History.id == history_id,
                                                History.time_in == None).update(
            {"time_in": dt}, synchronize_session='fetch')

    @staticmethod
    def reset(server_id):
        return db.session.query(History).filter(History.FlexLM_product.has(server_id=server_id),
                                                History.time_in == None).update(
            {'time_in': datetime.datetime.now().replace(second=0, microsecond=0)}, synchronize_session='fetch')

    @staticmethod
    def users_currently_checked_out(server_id):
        query = db.session.query(User).join(History).join(Product).filter(History.time_in == None,
                                                                          server_id=server_id).all()
        return query


# ----------------------------------------------------------------------------#
# Jsonify results
# ----------------------------------------------------------------------------#
class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)  # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)
