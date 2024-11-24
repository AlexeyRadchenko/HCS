
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, and_

from api.security.user_model import UserInDB, ManagementUserInDB
from ..database import row2dict
from .models import AccountUsers, AccountScopes, AccountUsersScopes

async def get_account_user_by_a_s_h_a(db: AsyncSession, account: str, street: str, house: str, appartment: str):
    result = await db.execute(
        select(AccountUsers)
        .where(
            and_(
                AccountUsers.account == account,
                AccountUsers.street == street,
                AccountUsers.house == house,
                AccountUsers.appartment == appartment
            )
        )
    )
    return result.scalar()

async def get_account_user_by_account(db: AsyncSession, account: str):
    result = await db.execute(
        select(AccountUsers)
        .where(AccountUsers.account == account)
    )
    return result.scalar() 