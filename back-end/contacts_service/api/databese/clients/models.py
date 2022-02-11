import uuid
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()



class ContactsAddresses(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    street = Column(String, index=True, nullable=False)
    house_number = Column(String, nullable=True)
    entrance = Column(String, nullable=True)
    appartment = Column(String, nullable=True)
    clients = relationship(
        'ContactsClients', secondary='clients_addresses', back_populates='addresses'
    )  
    
    
class ContactsClientOrganisations(Base):
    __tablename__ = "client_organisations"

    client_uuid = Column(Text(length=36), ForeignKey('clients.uuid'), primary_key=True) # for dev in sqlite
    #client_uuid = Column(UUID(as_uuid=True), ForeignKey('clients.uuid'), primary_key=True) # for postresql
    org_id = Column(Integer, ForeignKey('organisations.id'), primary_key=True)    

class ContactsClientsAddresses(Base):
    __tablename__ = "clients_addresses"
    client_uuid = Column(Text(length=36), ForeignKey('clients.uuid'), primary_key=True) # for dev in sqlite
    #client_uuid = Column(UUID(as_uuid=True), ForeignKey('clients.uuid'), primary_key=True) # for postresql
    address_id = Column(Integer, ForeignKey('addresses.id'), primary_key=True)
    full_owner = Column(Boolean, default=False)
    part_owner = Column(Boolean, default=False)
    part_size = Column(String, nullable=True)    


class ContactsEmails(Base):
    __tablename__ = "emails_msgers"
    
    id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    client_uuid = Column(Text(length=36), ForeignKey('clients.uuid'), nullable=True)
    email = Column(String, nullable=False)

class ContactsPhones(Base):
    __tablename__ = "phones"

    id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    client_uuid = Column(Text(length=36), ForeignKey('clients.uuid'), nullable=True)
    home_phone = Column(String, nullable=False)
    work_phone = Column(String, nullable=False)
    mobile_phone = Column(String, nullable=False)    


class ContactsOrganisations(Base):
    __tablename__ = "organisations"

    id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    full_name = Column(String(500), index=True, nullable=False)
    short_name = Column(String(300), nullable=True)
    clients = relationship(
        'ContactsClients', secondary='client_organisations', back_populates='organisations'

    )

class ContactsClients(Base):
    __tablename__ = "clients"

    uuid = Column(Text(length=36), primary_key=True, default=lambda: str(uuid.uuid4())) # for dev in sqlite
    #uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4) # for postresql
    name = Column(String, nullable=True)
    second_name = Column(String, nullable=True)
    surname = Column(String, nullable=True)
    phones = relationship(
        'ContactsPhones', backref='clients', lazy='joined'
    )
    emails = relationship(
        'ContactsEmails', backref='clients', lazy='joined'
    )
    note = Column(Text(), nullable=True)
    client_del = Column(Boolean, default=False)
    addresses = relationship(
        'ContactsAddresses', secondary='clients_addresses', back_populates='clients', lazy='joined'
    )
    organisations = relationship(
        'ContactsOrganisations', secondary='client_organisations', back_populates='clients', lazy='joined'
    )
   
