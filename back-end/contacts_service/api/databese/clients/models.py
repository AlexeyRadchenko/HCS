import uuid
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, DateTime, select
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

Base = declarative_base()



class ContactsAddresses(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    street = Column(String, index=True, nullable=False)
    house_number = Column(String, nullable=True)
    entrance = Column(String, nullable=True)
    appartment = Column(String, nullable=True)
    organisation_id = Column(Integer, ForeignKey('organisations.id'))

    """clients = relationship(
        'ContactsClients', secondary='clients_addresses', back_populates='addresses', lazy='dynamic'
    )"""
    clients = relationship('ContactsClientsAddresses', back_populates='address')
    #address_extend = relationship('ContactsClientsAddresses', backref='addresses', lazy='joined')


    
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
    address = relationship('ContactsAddresses', back_populates='clients', lazy='joined')
    client = relationship('ContactsClients', back_populates='addresses')

    @hybrid_property
    def address_data(self):
        return self.address
        

    @address_data.expression
    def owners(cls):
        return (select([ContactsAddresses]) 
                .where(ContactsAddresses.id == cls.address_id)) # ContactsClientsAddresses

class ContactsEmails(Base):
    __tablename__ = "emails_msgers"
    
    id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    client_uuid = Column(Text(length=36), ForeignKey('clients.uuid'), nullable=True)
    email = Column(String, nullable=False)

class ContactsPhones(Base):
    __tablename__ = "phones"

    id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    client_uuid = Column(Text(length=36), ForeignKey('clients.uuid'), nullable=True)
    #client_uuid = Column(UUID(as_uuid=True), ForeignKey('clients.uuid'), nullable=True)
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
    """
    addresses = relationship(
        'ContactsAddresses', backref='organisations', lazy='joined'
    )"""

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

    addresses = relationship('ContactsClientsAddresses', back_populates='clients', lazy='joined')

    """addresses = relationship(
        'ContactsAddresses', secondary='clients_addresses', back_populates='clients', lazy='joined'
    )"""
    
    organisations = relationship(
        'ContactsOrganisations', secondary='client_organisations', back_populates='clients', lazy='joined'
    )

    edit_journal = relationship('ContactsEditJournal', back_populates="clients", uselist=False)

class ContactsEditJournal(Base):
    __tablename__ = "edit_journal"
    
    id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    client_uuid = Column(Text(length=36), ForeignKey('clients.uuid'), nullable=False)
    date_create = Column(DateTime, nullable=False, server_default=func.now())
    date_update = Column(DateTime, nullable=True, onupdate=func.now())
    date_delete = Column(DateTime, nullable=True)
    who_make = Column(String, nullable=False)
    who_update = Column(String, nullable=True)
    who_delete = Column(String, nullable=True)

    clients = relationship('ContactsClients', back_populates="edit_journal", uselist=False)


"""
https://stackoverflow.com/questions/13370317/sqlalchemy-default-datetime
"""