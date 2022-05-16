from typing import Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import false, select, update, desc, cast, func, Integer
from sqlalchemy.orm import joinedload

from ..database import row2dict
from .models import Account


async def get_account_data_by_account(db: AsyncSession, account: str):
    result = await db.execute(
        select(
            Account
        )
        .where(Account.account == account)
    )
    return result.scalar()
