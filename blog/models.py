from re import S
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from database import Base
from sqlalchemy.orm import relationship


class Blog(Base):
    __tablename__="blog"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
    user_id = Column(Integer, ForeignKey('User.id'))
    creator = relationship('User', back_populates='blog')


class User(Base):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    blog = relationship('Blog', back_populates='creator')

