import sqlalchemy
from sqlalchemy import orm
from sqlalchemy.orm import relationship
from .db_session import SqlAlchemyBase


class Trans(SqlAlchemyBase):
    __tablename__ = 'trans'
    tr_id = sqlalchemy.Column(sqlalchemy.Integer,
                              primary_key=True, autoincrement=True)
    us_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("users.us_id"),
                              index=True, nullable=True)
    us_id_to = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("users.us_id"),
                                 index=True, nullable=True)
    sum = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    trans = relationship("Trans", back_populates='user')
    '''fr1 = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("users.id"), nullable=True)
    # fr1 = relationship('User')#надо ли релатион делать?
    restaurant_id = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    sum_all = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    participants = relationship("Participants", back_populates='user')'''
