from typing import Any, List, Optional
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import false, select, update, desc, cast, func, Integer, and_
from sqlalchemy.orm import joinedload, aliased
from datetime import datetime

from ..database import row2dict
from .models import Houses, Acts, Mainworks, Subworks, Fixworks, Actfiles, Smetafiles, Acthassubworks, Acthasfixworks


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
    #act_has_subworks = aliased(Acthassubworks)  # замените на название вашей промежуточной таблицы
    #act_has_fixworks = aliased(Acthasfixworks)
    result = await db.execute(
        select(
            Acts,
        )
        .where(Acts.house_id == id)
        .order_by(desc(Acts.id))
    )
    return result.scalar()

async def get_all_mkd_works_by_house_id(db: AsyncSession, id: int):
    result = await db.execute(
        select(
            Acts,
            Acthassubworks.sum,
        )
        .where(Acts.house_id == id)
    )
    return result.scalars().unique().all()

async def get_all_mainworks(db: AsyncSession):
    result = await db.execute(
        select(
            Mainworks
        )
    )
    return result.scalars().unique().all()

async def get_all_subworks(db: AsyncSession):
    result = await db.execute(
        select(
            Subworks
        )
    )
    return result.scalars().unique().all()

async def get_all_fixworks(db: AsyncSession):
    result = await db.execute(
        select(
            Fixworks
        )
    )
    return result.scalars().unique().all()