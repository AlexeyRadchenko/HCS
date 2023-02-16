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
    birth_place = Column(String, nullable=True)
    scan = Column(String, nullable=True)
    account_il = relationship("Accounts_il", back_populates="passport_il")


class Accounts_il(Base):
    __tablename__ = "accounts_il"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4) # for postresql
    account_number = Column(String, nullable=True)
    name = Column(String, nullable=True)
    second_name = Column(String, nullable=True)
    surname = Column(String, nullable=True)
    inn = Column(String, nullable=True)
    del_mark = Column(Boolean, default=False)
    part_of_appartment = Column(String, nullable=True)
    passport = Column(Integer, ForeignKey('passport_il.id'), nullable=True)
    passport_il = relationship('Passport_il', back_populates='account_il', lazy='joined')
    lists_il = relationship(
        'All_il', secondary='il_accounts', back_populates='accounts_il', lazy='dynamic'
    )
    payments_il = relationship('Payments_il', back_populates='account_il', lazy='joined')


class Egrn_il(Base):
    __tablename__ = "egrn_il"

    id = Column(BigInteger, primary_key=True, index=True, nullable=False, autoincrement=True)
    date = Column(DateTime, nullable=True)
    number = Column(String, nullable=True)
    name = Column(String, nullable=True)
    file = Column(String, nullable=True)
    note = Column(String, nullable=True)
    del_mark = Column(Boolean, default=False)
    il_id = Column(BigInteger, ForeignKey('all_il.id'), nullable=False)
    list_il = relationship("All_il", back_populates="egrn_il")


class Debt_calc_il(Base):
    __tablename__ = "debt_calc_il"

    id = Column(BigInteger, primary_key=True, index=True, nullable=False, autoincrement=True)
    final_sum = Column(DECIMAL(24,2), nullable=True)
    date = Column(DateTime, nullable=True)
    number = Column(String, nullable=True)
    file = Column(String, nullable=True)
    il_id = Column(BigInteger, ForeignKey('all_il.id'), nullable=False)
    list_il = relationship("All_il", back_populates="debt_sum_calc_il")   


class Debt_period_il(Base):
    __tablename__ = "debt_period_il"

    id = Column(BigInteger, primary_key=True, index=True, nullable=False, autoincrement=True)
    start_date = Column(DateTime, nullable=True)
    il_id = Column(BigInteger, ForeignKey('all_il.id'), nullable=False)
    list_il = relationship("All_il", back_populates="debt_period_time_il")  


class Judge_orders_il(Base):
    __tablename__ = "judge_orders_il"

    id = Column(BigInteger, primary_key=True, index=True, nullable=False, autoincrement=True)
    date = Column(DateTime, nullable=True)
    number = Column(String, nullable=True)
    file = Column(String, nullable=True)
    il_id = Column(BigInteger, ForeignKey('all_il.id'), nullable=False)
    list_il = relationship("All_il", back_populates="judge_order_date_il")


class Judge_orders_exec_il(Base):
    __tablename__ = "judge_orders_exec_il"

    id = Column(BigInteger, primary_key=True, index=True, nullable=False, autoincrement=True)
    date = Column(DateTime, nullable=True)
    number = Column(String, nullable=True)
    file = Column(String, nullable=True)
    il_id = Column(BigInteger, ForeignKey('all_il.id'), nullable=False)
    list_il = relationship("All_il", back_populates="judge_order_exec_date_il")        


class Payments_il(Base):
    __tablename__ = "payments_il"

    id = Column(BigInteger, primary_key=True, index=True, nullable=False, autoincrement=True)
    date =  Column(DateTime, nullable=False)
    type = Column(String, nullable=True)
    sum = Column(DECIMAL(24,2), nullable=False)
    who_paid_uuid = Column(UUID(as_uuid=True), ForeignKey('accounts_il.uuid'), nullable=True)
    notes = Column(Text(), nullable=True)
    il_id = Column(BigInteger, ForeignKey('all_il.id'), nullable=False)
    list_il = relationship("All_il", back_populates="payments_il")
    account_il = relationship("Accounts_il", back_populates="payments_il")


class Organisations_il(Base):
    __tablename__ = "organisations_il"
    id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    short_name = Column(String, nullable=True)
    full_name = Column(String, nullable=True)



class All_il(Base):
    __tablename__ = "all_il"

    id = Column(BigInteger, primary_key=True, index=True, nullable=False, autoincrement=True)
    street = Column(String, nullable=False)
    house = Column(String, nullable=False)
    appartment = Column(String, nullable=False)
    one_or_parts = Column(Boolean, default=True)
    property_self = Column(Boolean, default=True)
    il_number = Column(String, nullable=False)
    il_date = Column(DateTime, nullable=True)
    ur_in_work = Column(Boolean, default=False)
    gov_tax = Column(DECIMAL(12,2), nullable=True)
    order_cancel = Column(Boolean, default=False)
    bailiff_forward_date = Column(DateTime, nullable=True)
    start_exec_pross_date = Column(DateTime, nullable=True)
    end_exec_pross_date = Column(DateTime, nullable=True)
    # sum_all_get = Column(DECIMAL(24,2), nullable=True)
    # sum_not_yet_get = Column(DECIMAL(24,2), nullable=True)
    payments = Column(DECIMAL(24,2), nullable=True)
    debt_sum_il = Column(DECIMAL(24,2), nullable=True)
    notes = Column(Text(), nullable=True)
    organisation_id = Column(Integer, ForeignKey('organisations_il.id'), nullable=False)
    del_mark = Column(Boolean, default=False)

    egrn_il = relationship('Egrn_il', back_populates='list_il', lazy='joined')
    debt_sum_calc_il = relationship('Debt_calc_il', back_populates='list_il', lazy='joined')
    debt_period_time_il = relationship('Debt_period_il', back_populates='list_il', lazy='joined')
    judge_order_date_il = relationship('Judge_orders_il', back_populates='list_il', lazy='joined')
    judge_order_exec_date_il = relationship('Judge_orders_exec_il', back_populates='list_il', lazy='joined')
    payments_il = relationship('Payments_il', back_populates='list_il', lazy='joined')
    accounts_il = relationship(
        'Accounts_il', secondary='il_accounts', back_populates='lists_il', lazy='joined'
    )

    @hybrid_property
    def sum_all_get(self):
        return sum(payments.sum for payments in self.payments_il)

    #@sum_all_get.expression
    #def sum_all_get(cls):
        #return select(func.sum(Payments_il.sum)).\
        #where(Payments_il.il_id==cls.id)  #.label('total_sum_get')
        

    @hybrid_property
    def sum_not_yet_get(self):
        return self.debt_sum_il - self.sum_all_get


class IL_accounts(Base):
    __tablename__ = "il_accounts"

    il_id = Column(BigInteger, ForeignKey('all_il.id'), primary_key=True, nullable=False)
    account_uuid = Column(UUID(as_uuid=True), ForeignKey('accounts_il.uuid'), primary_key=True, nullable=False)
