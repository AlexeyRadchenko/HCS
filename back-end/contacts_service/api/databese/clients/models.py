from http import client
from msilib.schema import ComboBox
import uuid

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()

class ContactsAddress(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    street = Column(String, index=True, nullable=False)
    house_number = Column(String, nullable=True)
    entrance = Column(String, nullable=True)
    appartment = Column(String, nullable=True)
    client = relationship(
        'ContactsClients', secondary='clients_address', back_populates='address', uselist=False
    )  
    
    
class ContactsPhones(Base):
    __tablename__ = "phones"

    id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    home_phone = Column(String, nullable=False)
    work_phone = Column(String, nullable=False)
    mobile_phone = Column(String, nullable=False)

class ContactsEmails(Base):
    __tablename__ = "emails_msgers"

    id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    email = Column(String, nullable=False)

class ContactsClientsAddress(Base):
    __tablename__ = "clients_address"
    id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    client_uuid = Column(Text(length=36), ForeignKey('clients.uuid'), primary_key=True) # for dev in sqlite
    #client_uuid = Column(UUID(as_uuid=True), ForeignKey('clients.uuid'), primary_key=True) # for postresql
    address_id = Column(Integer, ForeignKey('address.id'), primary_key=True)
    full_owner = Column(Boolean, default=False)
    part_owner = Column(Boolean, default=False)
    part_size = Column(String, nullable=True) 

class ContactsClients(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    uuid = Column(Text(length=36), primary_key=True, default=lambda: str(uuid.uuid4())) # for dev in sqlite
    #uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4) # for postresql
    name = Column(String, nullable=True)
    second_name = Column(String, nullable=True)
    surname = Column(String, nullable=True)
    phones = Column(Integer, ForeignKey('phones.id'))
    emails = Column(Integer, ForeignKey('emails_msgers.id'))
    note = Column(Text(), nullable=True)
    addresses = relationship(
        'ContactsAddress', secondary='clients_address', back_populates='clients', uselist=False
    )
    