from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, DateTime, func, create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from config import SQLALCHEMY_DATABASE_URI

engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Server(Base):
    __tablename__ = 'flexlm_server'
    id = Column(Integer, primary_key=True)
    name = Column(String(35), nullable=False, unique=True)
    port = Column(String(10), nullable=False)

    def __init__(self, name, port):
        self.name = name
        self.port = port

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


class Update(Base):
    __tablename__ = 'flexlm_update'
    id = Column(Integer, primary_key=True)
    server_id = Column(Integer, ForeignKey("flexlm_server.id"), nullable=False)
    status = Column(String(8))
    info = Column(String(255), default=None)
    time_start = Column(DateTime, default=func.now())
    time_complete = Column(DateTime, default=None)
    FlexLM_server = relationship(u'Server')

    def __init__(self, server_id, status, info):
        self.server_id = server_id
        self.status = status
        self.info = info

    @staticmethod
    def start(server_id):
        insert = Update(server_id=server_id, status='UPDATING', info=None)
        session.add(insert)
        session.commit()
        return insert.id

    @staticmethod
    def end(update_id, status=None, info=None):
        session.query(Update).filter_by(id=update_id).update({"status": status,
                                                              "info": info,
                                                              "time_complete": datetime.now()},
                                                             synchronize_session='fetch')
        session.commit()
        session.close()


class Product(Base):
    __tablename__ = 'flexlm_product'
    __table_args__ = (
        UniqueConstraint('server_id', 'internal_name', name='UQ_server_internalname'),
        UniqueConstraint('server_id', 'common_name', name='UQ_server_commonname'),
    )
    id = Column(Integer, primary_key=True)
    server_id = Column(Integer, ForeignKey("flexlm_server.id"), nullable=False)
    internal_name = Column(String(35), nullable=False)
    common_name = Column(String(35), nullable=False)
    category = Column(String(35), nullable=False)
    type = Column(String(10), nullable=False)
    license_out = Column(Integer)
    license_total = Column(Integer)
    FlexLM_server = relationship(u'Server')

    def __init__(self, server_id, internal_name, **kwargs):
        self.server_id = server_id
        self.internal_name = internal_name
        super(Product, self).__init__(**kwargs)

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


class Workstation(Base):
    __tablename__ = 'flexlm_workstation'
    id = Column(Integer, primary_key=True)
    name = Column(String(25), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

    @staticmethod
    def exists_or_insert(workstation):
        w = session.query(Workstation).filter_by(name=workstation).first()
        if w is None:
            w = Workstation(name=workstation)
            session.add(w)
            session.commit()
        return w.id


class User(Base):
    __tablename__ = 'flexlm_user'
    id = Column(Integer, primary_key=True)
    name = Column(String(25), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

    @staticmethod
    def exists_or_insert(user):
        u = session.query(User).filter_by(name=user).first()
        if u is None:
            u = User(name=user)
            session.add(u)
            session.commit()
        return u.id

    @staticmethod
    def distinct_users():
        return session.query(User.name).distinct().all()


class History(Base):
    __tablename__ = 'flexlm_history'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("flexlm_user.id"), nullable=False)
    workstation_id = Column(Integer, ForeignKey("flexlm_workstation.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("flexlm_product.id"), nullable=False)
    update_id = Column(Integer, ForeignKey("flexlm_update.id"), nullable=False)
    time_out = Column(DateTime, nullable=False)
    time_in = Column(DateTime, nullable=True)
    FlexLM_product = relationship(u'Product')
    FlexLM_update = relationship(u'Update')
    FlexLM_user = relationship(u'User')
    FlexLM_workstation = relationship(u'Workstation')

    def __init__(self, user_id, workstation_id, product_id, update_id, time_out, time_in):
        self.user_id = user_id
        self.workstation_id = workstation_id
        self.product_id = product_id
        self.update_id = update_id
        self.time_out = time_out
        self.time_in = time_in

    @staticmethod
    def exists_or_insert(user_id, workstation_id, server_id, product_id, update_id, time_out):
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
            {'time_in': datetime.now().replace(second=0, microsecond=0)}, synchronize_session='fetch')

    @staticmethod
    def users_currently_checked_out(server_id):
        query = session.query(User).join(History).join(Product).filter(History.time_in == None,
                                                                       server_id=server_id).all()
        return query
