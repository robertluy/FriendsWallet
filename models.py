
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, MetaData
from sqlalchemy.orm import relationship
from db_control import SqlAlchemyBase
import datetime

metadata_obj = MetaData()


class Debts(SqlAlchemyBase):
    __tablename__ = 'debts'
    date_d = Column(DateTime, default=datetime.datetime.utcnow, primary_key=True, index=True)
    us_id_to = Column(Integer, ForeignKey("users.us_id"), primary_key=True, index=True, nullable=False)
    us_id = Column(Integer, ForeignKey("users.us_id"), primary_key=True, index=True, nullable=False)
    debt = Column(Float, nullable=False)
    status = Column(String, nullable=False)

    user_to = relationship("User", foreign_keys=[us_id_to], back_populates="debts_to")
    user_from = relationship("User", foreign_keys=[us_id], back_populates="debts_from")


class User(SqlAlchemyBase):
    __tablename__ = 'users'
    us_id = Column(Integer, primary_key=True, autoincrement=True)
    tg_tag = Column(String, nullable=False, index=True, unique=True)
    tg_id = Column(String, nullable=True)
    wallet = Column(String, nullable=True)
    created_date = Column(DateTime, default=datetime.datetime.now)

    # Отношения с таблицей Debts
    debts_to = relationship("Debts", back_populates="user_to", foreign_keys="Debts.us_id_to")
    debts_from = relationship("Debts", back_populates="user_from", foreign_keys="Debts.us_id")
