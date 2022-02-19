from ast import Constant
from multiprocessing.connection import Client
from typing import Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, desc, distinct
from sqlalchemy.orm import joinedload

from ..database import row2dict
from .models import ContactsAddresses, ContactsClients, ContactsClientsAddresses, ContactsPhones, ContactsOrganisations, ContactsEmails

async def update_contacts_client_by_uuid(
    db: AsyncSession, 
    client: ContactsClients, 
    client_phones: ContactsPhones, 
    client_emails: ContactsEmails,
    uuid: str
    ):

    client_values = row2dict(client)
    client_values.pop('uuid', None)
    client_values.pop('client_del', None)

    await db.execute(
        update(ContactsClients)
        .where(ContactsClients.uuid == uuid)
        .values(client_values)
    )
    client_phones_values = row2dict(client_phones)
    client_phones_values.pop('id', None)
    client_phones_values.pop('client_uuid', None)
    await db.execute(
        update(ContactsPhones)
        .where(ContactsPhones.client_uuid == uuid)
        .values(client_phones_values)
    )
    client_emails_values = row2dict(client_emails)
    client_emails_values.pop('id', None)
    client_emails_values.pop('client_uuid', None)
    await db.execute(
        update(ContactsEmails)
        .where(ContactsEmails.client_uuid == uuid)
        .values(client_emails_values)
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

async def get_contacts_clients_list(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(
            ContactsClients
        ))
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