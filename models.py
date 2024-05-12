
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, MetaData
from sqlalchemy.orm import relationship
from db_control import SqlAlchemyBase
import datetime

metadata_obj = MetaData()


class Debts(SqlAlchemyBase):
    __tablename__ = 'debts'
    date_d = Column(DateTime, default=datetime.datetime.utcnow, primary_key=True, index=True)
    tg_id_to = Column(Integer, ForeignKey("users.us_id"), primary_key=True, index=True, nullable=False)
    tg_id = Column(Integer, ForeignKey("users.us_id"), primary_key=True, index=True, nullable=False)
    debt = Column(Float, nullable=False)
    status = Column(String, nullable=False)
    currency = Column(String, nullable=False)

    tg_to = relationship("User", foreign_keys=[tg_id_to], back_populates="debts_to")
    tg_from = relationship("User", foreign_keys=[tg_id], back_populates="debts_from")


class User(SqlAlchemyBase):
    __tablename__ = 'users'
    tg_id = Column(String, nullable=True, primary_key=True, unique=True)
    tg_tag = Column(String, nullable=False, index=True, unique=True)
    wallet = Column(String, nullable=True)
    created_date = Column(DateTime, default=datetime.datetime.now)

    # Отношения с таблицей Debts
    debts_to = relationship("Debts", back_populates="tg_to", foreign_keys="Debts.tg_id_to")
    debts_from = relationship("Debts", back_populates="tg_from", foreign_keys="Debts.tg_id")
