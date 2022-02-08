from operator import add
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from ..database import row2dict
from .models import ContactsAddress, ContactsClients

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
    """result = await db.execute(
        select(ContactsClients, ManagementScopes.scope_name.label('scopes'))
        .join(ManagementScopes, ManagementUsers.management_scopes).offset(skip).limit(limit))
    return result.all()"""
    pass

async def create_contacts_user(db: AsyncSession, user: ContactsClients):
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def create_contacts_address(db: AsyncSession, address: ContactsAddress):
    db.add(address)
    await db.commit()
    await db.refresh(address)
    return address