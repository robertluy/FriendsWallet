import sqlalchemy
import datetime
from sqlalchemy import orm
from sqlalchemy.orm import relationship
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'
    us_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    tg_tag = sqlalchemy.Column(sqlalchemy.String, nullable=False, index=True, unique=True)
    tg_id = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    wallet = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
