from operator import add
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from ..database import row2dict
from .models import ContactsAddress, ContactsClients, ContactsEmails, ContactsPhones, ContactsOrganisations

"""async def get_management_user(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(ManagementUsers, ManagementScopes.scope_name, ManagementScopes.active_scope)
        .join(ManagementScopes, ManagementUsers.management_scopes).where(ManagementUsers.id == user_id)
    )
    return result.scalars().all()


async def get_management_user_by_login(db: AsyncSession, login: str):
    result = await db.execute(
        select(ManagementUsers, ManagementScopes.scope_name.label('scopes'))
        .join(ManagementScopes, ManagementUsers.management_scopes).where(ManagementUsers.login == login)
    )
    return result.all()"""


async def get_contacts_clients(db: AsyncSession, skip: int = 0, limit: int = 100):
    """select(
            ContactsClients, ContactsPhones.home_phone.label('home_phone'), ContactsPhones.work_phone.label('work_phone'),
            ContactsPhones.mobile_phone.label('mobile_phone'), ContactsEmails.email.label('emails'),
            ContactsAddress, ContactsOrganisations
        )
        .join(ContactsPhones)
        .join(ContactsEmails)
        .join(ContactsAddress)
        .join(ContactsOrganisations)
        .limit(limit)"""
    result = await db.execute(
        select(
            ContactsClients, ContactsPhones.work_phone.label('work_phones')
        )
        .join(ContactsPhones, ContactsClients.phones == ContactsPhones.id)
        .offset(skip).limit(limit)
        )
    return result.all()


async def create_contacts_db_oject(db: AsyncSession, obj: Any):
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj
