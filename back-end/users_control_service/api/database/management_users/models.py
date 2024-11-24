from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ManagementUsersScopes(Base):
    __tablename__ = "management_users_scopes"
    notes = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey('management_users.id'), primary_key=True)
    scope_id = Column(Integer, ForeignKey('management_scopes.id'), primary_key=True)


class ManagementUsers(Base):
    __tablename__ = "management_users"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    login = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    second_name = Column(String, nullable=True)
    surname = Column(String, nullable=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    management_scopes = relationship(
        'ManagementScopes', secondary='management_users_scopes', back_populates='management_users', uselist=False
    )
    
class ManagementScopes(Base):
    __tablename__ = "management_scopes"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    scope_name = Column(String, unique=True, nullable=False)
    active_scope = Column(Boolean, default=True)
    management_users = relationship(
        'ManagementUsers', secondary='management_users_scopes', back_populates='management_scopes', uselist=False
    ) 
