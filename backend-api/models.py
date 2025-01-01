from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from geoalchemy2 import Geometry

Base = declarative_base()

class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(Text)
    lat = Column(String)
    lng = Column(String)
    delivery_deadline = Column(DateTime)

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id'))
    status = Column(String, default='PENDING')
    created_at = Column(DateTime, default=func.now())

class Route(Base):
    __tablename__ = 'routes'
    id = Column(Integer, primary_key=True)
    start_location = Column(Geometry('POINT', 4326))
    end_location = Column(Geometry('POINT', 4326))
    route_data = Column(JSONB)

class RouteStep(Base):
    __tablename__ = 'route_steps'
    id = Column(Integer, primary_key=True)
    route_id = Column(Integer, ForeignKey('routes.id'))
    step_index = Column(Integer)
    client_id = Column(Integer, ForeignKey('clients.id'))
