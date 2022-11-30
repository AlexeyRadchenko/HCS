from typing import Any, List, Optional
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import false, select, update, desc, cast, func, Integer, and_
from sqlalchemy.orm import joinedload
from datetime import datetime

from ..database import row2dict
from .models import All_il, Accounts_il

async def create_debt_il_object(db: AsyncSession, debt_il_object: Any):
    db.add(debt_il_object),
    await db.commit()
    await db.refresh(debt_il_object)
    return debt_il_object

async def get_all_il_data_list(db: AsyncSession):
    result = await db.execute(
        select(
            All_il
        ).where(All_il.del_mark == False)
    )
    return result.scalars().unique().all()

async def get_all_fio_from_db(db: AsyncSession):
    result = await db.execute(
        select(
            Accounts_il
        )
    )
    return result.scalars().unique().all()