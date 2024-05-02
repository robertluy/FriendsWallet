import sqlalchemy
import datetime
from sqlalchemy import orm
from sqlalchemy.orm import relationship
from .db_session import SqlAlchemyBase
from .users import User


class Debts(SqlAlchemyBase):
    __tablename__ = 'debts'
    date_d = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now, primary_key=True, index=True)
    us_id_to = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.us_id"), primary_key=True, index=True,
                                 nullable=False)
    us_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.us_id"), primary_key=True, index=True,
                              nullable=False)
    debt = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    status = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    user = relationship("User", foreign_keys=[us_id_to])
    user2 = relationship("User", foreign_keys=[us_id])
