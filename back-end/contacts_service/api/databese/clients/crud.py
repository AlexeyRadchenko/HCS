from ast import Constant
from multiprocessing.connection import Client
from typing import Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import false, select, update, desc, cast, Integer
from sqlalchemy.orm import joinedload

from ..database import row2dict
from .models import ContactsAddresses, ContactsClients, ContactsClientsAddresses, ContactsEditJournal, ContactsPhones, ContactsOrganisations, ContactsEmails

async def update_contacts_client_by_uuid(
    db: AsyncSession, 
    client: ContactsClients, 
    client_journal: ContactsEditJournal,
    uuid: str,
    client_phones: Optional[ContactsPhones]=None, 
    client_emails: Optional[ContactsEmails]=None,
    ):

    client_values = row2dict(client)
    client_values.pop('uuid', None)
    client_values.pop('client_del', None)

    await db.execute(
        update(ContactsClients)
        .where(ContactsClients.uuid == uuid)
        .values(client_values)
    )
    if client_phones:
        client_phones_values = row2dict(client_phones)
        client_phones_values.pop('id', None)
        client_phones_values.pop('client_uuid', None)
        await db.execute(
            update(ContactsPhones)
            .where(ContactsPhones.client_uuid == uuid)
            .values(client_phones_values)
        )
    if client_emails:
        client_emails_values = row2dict(client_emails)
        client_emails_values.pop('id', None)
        client_emails_values.pop('client_uuid', None)
        await db.execute(
            update(ContactsEmails)
            .where(ContactsEmails.client_uuid == uuid)
            .values(client_emails_values)
        )
    client_journal_values = row2dict(client_journal)
    client_journal_values.pop('id', None)
    client_journal_values.pop('client_uuid', None)
    await db.execute(
        update(ContactsEditJournal)
        .where(ContactsEditJournal.client_uuid == uuid)
        .values(who_update=client_journal_values['who_update'])
    )
    await db.commit()
    return client

async def get_contacts_client_by_uuid(db: AsyncSession, uuid: str):
    result = await db.execute(
        select(
            ContactsClients
        )
        .options(
            joinedload(ContactsClients.phones),
            joinedload(ContactsClients.emails),
            joinedload(ContactsClients.addresses),
            joinedload(ContactsClients.organisations)
        )
        .join(ContactsPhones, ContactsClients.phones)
        .join(ContactsEmails, ContactsClients.emails)
        .join(ContactsAddresses, ContactsClients.addresses)
        .join(ContactsOrganisations, ContactsClients.organisations)
        .where(ContactsClients.uuid == uuid)
    )
    return result.scalar()

async def get_client_by_name_secondname_surname (db: AsyncSession, name, second_name, surname):
    result = await db.execute(
        select(
            ContactsClients
        )
        .where(ContactsClients.name == name, ContactsClients.second_name == second_name, ContactsClients.surname == surname)
    )
    return result.scalar()

async def get_contacts_clients_list(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(
            ContactsClients
        )
        .join(ContactsClientsAddresses, ContactsClients.addresses)
        .join(ContactsAddresses, ContactsClientsAddresses.address)
        .where(ContactsClients.client_del == False)
        .order_by(ContactsAddresses.street, ContactsAddresses.house_number, ContactsAddresses.entrance, ContactsAddresses.appartment) #cast(ContactsAddresses.appartment, Integer) not work in postgresql
        ) #.offset(skip).limit(limit)) #desc(ContactsAddresses.street), desc(ContactsAddresses.house_number), 
    return result.scalars().unique().all()

async def create_contacts_db_oject(db: AsyncSession, obj: Any):
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj

async def get_addressess_house_street_from_db_by_org_id(db, id: int):
    result = await db.execute(
        select(
            ContactsAddresses.street, ContactsAddresses.house_number, ContactsAddresses.organisation_id
        )
        .where(ContactsAddresses.organisation_id == id)
        .order_by(desc(ContactsAddresses.street), desc(ContactsAddresses.house_number))
    )
    return result.unique().all()

async def get_address_id_by_street_house_appartment (db, street, house, appartment):
    result = await db.execute(
        select(
            ContactsAddresses.id
        )
        .where(ContactsAddresses.street == street, ContactsAddresses.house_number == house, ContactsAddresses.appartment == appartment)
    )
    return result.scalar()

async def delete_contacts_client_by_uuid(db, uuid, client_journal):
    await db.execute(
        update(ContactsClients)
        .where(ContactsClients.uuid == uuid)
        .values(client_del=True)
    )
    client_journal_values = row2dict(client_journal)
    client_journal_values.pop('id', None)
    client_journal_values.pop('client_uuid', None)
    await db.execute(
        update(ContactsEditJournal)
        .where(ContactsEditJournal.client_uuid == uuid)
        .values(who_delete=client_journal_values['who_delete'])
    )
    await db.commit()