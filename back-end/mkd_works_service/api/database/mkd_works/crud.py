from typing import Any, List, Optional
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import false, select, update, desc, cast, func, Integer, and_
from sqlalchemy.orm import joinedload
from datetime import datetime

from ..database import row2dict
from .models import Houses, Acts


async def create_mkd_works_db_object(db: AsyncSession, obj: Any):
    db.add(obj),
    await db.commit()
    await db.refresh(obj)
    return obj

async def get_all_houses(db: AsyncSession):
    result = await db.execute(
        select(
            Houses
        )
    )
    return result.scalars().unique().all()

async def get_furure_work_id_from_db(db: AsyncSession, id: int):
    result = await db.execute(
        select(
            Acts
        )
        .where(Acts.house_id == id)
        .order_by(desc(Acts.id))
    )
    return result.scalar()

async def get_all_mkd_works_by_house_id(db: AsyncSession, id: int):
    result = await db.execute(
        select(
            Acts
        )
        .where(Acts.house_id == id)
        #.order_by(desc(ContactsAddresses.street), desc(ContactsAddresses.house_number))
    )
    return result.scalars().unique().all()