from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from api.security.user_model import UserInDB, ManagementUserInDB
from ..database import row2dict
from .models import ManagementUsers, ManagementScopes, ManagementUsersScopes

async def get_management_user(db: AsyncSession, user_id: int):
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
    return result.all()


async def get_management_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(ManagementUsers, ManagementScopes.scope_name.label('scopes'))
        .join(ManagementScopes, ManagementUsers.management_scopes).offset(skip).limit(limit))
    return result.all()

async def create_management_user(db: AsyncSession, user: ManagementUsers):
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def create_superuser(db: AsyncSession, login: str, password: str):
    super_user = ManagementUsers(login=login, hashed_password=password, is_superuser=True)
    db.add(super_user)
    await db.commit()
    await db.refresh(super_user)
    return super_user

async def update_management_user(db:AsyncSession, user: UserInDB):
    values = user.dict()
    update_user = ManagementUsers()
    await db.execute(update(ManagementUsers).where(ManagementUsers.id == user.id).values(values))
    await db.commit()
    await db.refresh(update_user)
    return update_user