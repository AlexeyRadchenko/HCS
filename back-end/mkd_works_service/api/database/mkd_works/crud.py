from typing import Any, List, Optional
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import false, select, update, desc, cast, func, Integer, and_
from sqlalchemy.orm import joinedload
from datetime import datetime

from ..database import row2dict
from .models import Houses


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