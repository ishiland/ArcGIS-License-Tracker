from config import SQLALCHEMY_DATABASE_URI
import datetime
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.declarative import DeclarativeMeta
import json
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa

base = declarative_base()
engine = sa.create_engine(SQLALCHEMY_DATABASE_URI)
base.metadata.bind = engine
session = orm.scoped_session(orm.sessionmaker())(bind=engine)


class Server(base):
    __tablename__ = 'server'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(35), nullable=False, unique=True)
    port = sa.Column(sa.String(10), nullable=False)

    def __init__(self, name, port):
        self.name = name
        self.port = port

    def __repr__(self):
        return '<Server %r>' % self.name

    @staticmethod
    def upsert(s):
        p = session.query(Server).filter(Server.name == s['name']).first()
        if p is None:
            p = Server(name=s['name'],
                       port=s['port'])
            session.add(p)
        else:
            p.port = s['port']
        session.commit()
        return p.id


class Updates(base):
    __tablename__ = 'updates'

    id = sa.Column(sa.Integer, primary_key=True)
    server_id = sa.Column(sa.Integer, sa.ForeignKey("server.id"), nullable=False)
    status = sa.Column(sa.String(8))
    info = sa.Column(sa.String(255), default=None)
    time_start = sa.Column(sa.DateTime)
    time_complete = sa.Column(sa.DateTime, default=None)
    FlexLM_server = orm.relationship(u'Server')

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
        session.add(insert)
        session.commit()
        return insert.id

    @staticmethod
    def end(update_id, status=None, info=None):
        session.query(Updates).filter_by(id=update_id).update({"status": status,
                                                               "info": info,
                                                               "time_complete": datetime.datetime.now()},
                                                              synchronize_session='fetch')
        session.commit()
        session.close()


class Product(base):
    __tablename__ = 'product'

    __table_args__ = (
        sa.UniqueConstraint('server_id', 'internal_name', name='UQ_server_internalname'),
        sa.UniqueConstraint('server_id', 'common_name', name='UQ_server_commonname'),
    )
    id = sa.Column(sa.Integer, primary_key=True)
    server_id = sa.Column(sa.Integer, sa.ForeignKey("server.id"), nullable=False)
    internal_name = sa.Column(sa.String(35), nullable=False)
    common_name = sa.Column(sa.String(35), nullable=False)
    category = sa.Column(sa.String(35), nullable=False)
    type = sa.Column(sa.String(10), nullable=False)
    license_out = sa.Column(sa.Integer)
    license_total = sa.Column(sa.Integer)
    FlexLM_server = orm.relationship(u'Server')

    def __init__(self, server_id, internal_name, **kwargs):
        self.server_id = server_id
        self.internal_name = internal_name
        super(Product, self).__init__(**kwargs)

    def __repr__(self):
        return '<Product %r>' % self.common_name

    @staticmethod
    def reset(server_id):
        session.query(Product).filter_by(server_id=server_id).update({"license_out": 0})
        session.flush()

    @staticmethod
    def upsert(server_id, internal_name, **kwargs):
        p = session.query(Product).filter_by(internal_name=internal_name, server_id=server_id).update(kwargs)
        if p == 0:
            p = Product(server_id=server_id,
                        internal_name=internal_name,
                        **kwargs)
            session.add(p)
            session.commit()
        return p

    @staticmethod
    def query(internal_name, server_id):
        p = session.query(Product).filter_by(internal_name=internal_name, server_id=server_id).first()
        return p.id


class Workstation(base):
    __tablename__ = 'workstation'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(25), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Workstation %r>' % self.name

    @staticmethod
    def add(workstation):
        w = session.query(Workstation).filter_by(name=workstation).first()
        if w is None:
            w = Workstation(name=workstation)
            session.add(w)
            session.commit()
        return w.id


class User(base):
    __tablename__ = 'user'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(25), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<User %r>' % self.name

    @staticmethod
    def add(username):
        u = session.query(User).filter_by(name=username).first()
        if u is None:
            u = User(name=username)
            session.add(u)
        session.commit()
        return u.id

    @staticmethod
    def delete(name):
        User.query.filter_by(name=name).delete()
        session.commit()

    @staticmethod
    def distinct_users():
        return session.query(User.name).distinct().all()


class History(base):
    __tablename__ = 'history'

    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey("user.id"), nullable=False)
    workstation_id = sa.Column(sa.Integer, sa.ForeignKey("workstation.id"), nullable=False)
    product_id = sa.Column(sa.Integer, sa.ForeignKey("product.id"), nullable=False)
    update_id = sa.Column(sa.Integer, sa.ForeignKey("updates.id"), nullable=False)
    time_out = sa.Column(sa.DateTime, nullable=False)
    time_in = sa.Column(sa.DateTime, nullable=True)
    FlexLM_product = orm.relationship(u'Product')
    FlexLM_update = orm.relationship(u'Updates')
    FlexLM_user = orm.relationship(u'User')
    FlexLM_workstation = orm.relationship(u'Workstation')

    def __init__(self, user_id, workstation_id, product_id, update_id, time_out, time_in):
        self.user_id = user_id
        self.workstation_id = workstation_id
        self.product_id = product_id
        self.update_id = update_id
        self.time_out = time_out
        self.time_in = time_in

    def __repr__(self):
        return '<History %r>' % self.id

    @hybrid_property
    def calculated_timein(self):
        if self.time_in:
            return self.time_in
        else:
            return datetime.datetime.now()

    @staticmethod
    def add(user_id, workstation_id, server_id, product_id, update_id, time_out):
        h = session.query(History).filter_by(user_id=user_id,
                                             workstation_id=workstation_id,
                                             product_id=product_id,
                                             time_in=None).join(Product).filter_by(server_id=server_id).first()
        if h is None:
            h = History(user_id=user_id,
                        workstation_id=workstation_id,
                        product_id=product_id,
                        update_id=update_id,
                        time_out=time_out,
                        time_in=None)
            session.add(h)
            session.flush()
        return h.id

    @staticmethod
    def time_in_none(server_id):
        t = session.query(History).filter_by(time_in=None).join(Product).filter_by(server_id=server_id).all()
        return t

    @staticmethod
    def update(history_id, dt, server_id):
        return session.query(History).filter(History.FlexLM_product.has(server_id=server_id),
                                             History.id == history_id,
                                             History.time_in == None).update(
            {"time_in": dt}, synchronize_session='fetch')

    @staticmethod
    def reset(server_id):
        return session.query(History).filter(History.FlexLM_product.has(server_id=server_id),
                                             History.time_in == None).update(
            {'time_in': datetime.datetime.now().replace(second=0, microsecond=0)}, synchronize_session='fetch')

    @staticmethod
    def users_currently_checked_out(server_id):
        query = session.query(User).join(History).join(Product).filter(History.time_in == None,
                                                                       server_id=server_id).all()
        return query


# ----------------------------------------------------------------------------#
# Jsonify results - utility for Flask
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
