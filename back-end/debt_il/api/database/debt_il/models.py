import uuid
from sqlalchemy import BigInteger, Boolean, Column, ForeignKey, Integer, String, Text, DateTime, select, DECIMAL
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

Base = declarative_base()


class Passport_il(Base):
    __tablename__ = "passport_il"

    id = Column(BigInteger, primary_key=True, index=True, nullable=False, autoincrement=True)
    serial = Column(String, nullable=False)
    number = Column(String, nullable=False)
    who_take = Column(String, nullable=True)
    date_take = Column(DateTime, nullable=True)
    squad_code = Column(String, nullable=True)
    birth_date = Column(DateTime, nullable=True)
    birth_city = Column(String, nullable=True)
    scan = Column(String, nullable=True)
    account_il = relationship("Account_il", back_populates="passport")


class Egrn_il(Base):
    __tablename__ = "egrn_il"

    id = Column(BigInteger, primary_key=True, index=True, nullable=False, autoincrement=True)
    date = Column(DateTime, nullable=True)
    number = Column(String, nullable=True)
    file = Column(String, nullable=True)
    account_il = relationship("Account_il", back_populates="egrn")


class Debt_calc_il(Base):
    __tablename__ = "debt_calc_il"

    id = Column(BigInteger, primary_key=True, index=True, nullable=False, autoincrement=True)
    final_sum = Column(DECIMAL(24,2), nullable=True)
    date = Column(DateTime, nullable=True)
    number = Column(String, nullable=True)
    file = Column(String, nullable=True)
    account_il = relationship("Account_il", back_populates="debt_sum_calc")   


class Debt_period_il(Base):
    __tablename__ = "debt_period_il"

    id = Column(BigInteger, primary_key=True, index=True, nullable=False, autoincrement=True)
    start_date = Column(DateTime, nullable=True)
    account_il = relationship("Account_il", back_populates="debt_period")  


class Judge_orders_il(Base):
    __tablename__ = "judge_orders_il"

    id = Column(BigInteger, primary_key=True, index=True, nullable=False, autoincrement=True)
    date = Column(DateTime, nullable=True)
    number = Column(String, nullable=True)
    file = Column(String, nullable=True)
    account_il = relationship("Account_il", back_populates="judge_order_date")


class Judge_orders_exec_il(Base):
    __tablename__ = "judge_orders_exec_il"

    id = Column(BigInteger, primary_key=True, index=True, nullable=False, autoincrement=True)
    date = Column(DateTime, nullable=True)
    number = Column(String, nullable=True)
    file = Column(String, nullable=True)
    account_il = relationship("Account_il", back_populates="judge_order_exec_date")    


class Accounts_il(Base):
    __tablename__ = "accounts_il"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4) # for postresql
    street = Column(String, nullable=False)
    house = Column(String, nullable=False)
    appartment = Column(String, nullable=False)
    property_self = Column(Boolean, default=True)
    name = Column(String, nullable=True)
    second_name = Column(String, nullable=True)
    surname = Column(String, nullable=True)
    birth_date = Column(DateTime, nullable=True)
    passport = Column(Integer, ForeignKey('passport_il.id'), nullable=True)
    egrn = Column(Integer, ForeignKey('egrn_il.id'), nullable=True)
    debt_sum_calc = Column(Integer, ForeignKey('debt_calc_il.id'), nullable=True)
    debt_period = Column(Integer, ForeignKey('debt_period_il.id'), nullable=True)
    ur_in_work = Column(Boolean, default=False)
    judge_order_date = Column(Integer, ForeignKey('judge_orders_il.id'), nullable=True)
    judge_order_exec_date = Column(Integer, ForeignKey('judge_orders_exec_il.id'), nullable=True)
    gov_tax = Column(DECIMAL(12,2), nullable=True)
    order_cancel = Column(Boolean, default=False)
    bailiff_forward_date = Column(DateTime, nullable=True)
    start_exec_pross_date = Column(DateTime, nullable=True)
    sum_all_get = Column(DECIMAL(24,2), nullable=True)
    sum_not_yet_get = Column(DECIMAL(24,2), nullable=True)
    notes = Column(Text(), nullable=True)


    """clients = relationship(
        'ContactsClients', secondary='clients_addresses', back_populates='addresses', lazy='dynamic'
    )"""
    #clients = relationship('ContactsClientsAddresses', back_populates='address')
    #address_extend = relationship('ContactsClientsAddresses', backref='addresses', lazy='joined')