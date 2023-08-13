from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserModel(Base):
    __tablename__ = "users"
    __table_args__ = {'schema': 'data'}
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    fullname = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=True)


class ProductModel(Base):
    __tablename__ = "products"
    __table_args__ = {'schema': 'data'}
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)


