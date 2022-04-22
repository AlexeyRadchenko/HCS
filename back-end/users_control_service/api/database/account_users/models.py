from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class AccountUsers(Base):
    __tablename__ = "account_users"

    id = Column(BigInteger, primary_key=True, index=True, nullable=False)
    account = Column(String, index=True, nullable=False)
    name = Column(String, nullable=True)
    second_name = Column(String, nullable=True)
    surname = Column(String, nullable=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    street = Column(String, nullable=True)
    house = Column(String, nullable=True)
    appartment = Column(String, nullable=True)
    account_scopes = relationship(
        'AccountScopes', secondary='account_users_scopes', lazy='joined'
    )
    

class AccountScopes(Base):
    __tablename__ = "account_scopes"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    scope_name = Column(String, unique=True, nullable=False)
    active_scope = Column(Boolean, default=True)


class AccountUsersScopes(Base):
    __tablename__ = "account_users_scopes"
    notes = Column(String, nullable=True)
    account_id = Column(Integer, ForeignKey('account_users.id'), primary_key=True)
    scope_id = Column(Integer, ForeignKey('account_scopes.id'), primary_key=True)