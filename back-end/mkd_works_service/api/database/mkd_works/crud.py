from typing import Any, List, Optional
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func
from sqlalchemy import false, select, update, desc, cast, func, Integer, and_
from sqlalchemy.orm import joinedload, aliased
from datetime import datetime

from ..database import row2dict
from .models import Houses, Acts, Mainworks, Subworks, Fixworks, Actfiles, Smetafiles, Acthassubworks, Acthasfixworks, YearActfiles, BGTasks


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

async def update_act_db(db: AsyncSession, obj: Acts):
    result = await db.execute(
        update(
            Acts
        )
        .values(
            num=obj.num,
            all_sum=obj.all_sum,
            month_year_works=obj.month_year_works,
            house_id=obj.house_id,
            director=obj.director,
            director_appartment=obj.director_appartment
        )
        .where(Acts.id == obj.id)
    )
    await db.commit()
    return result.rowcount

async def update_acthassubworks_db(db: AsyncSession, obj: Acthassubworks):
    result = await db.execute(
        update(
            Acthassubworks
        )
        .values(
            sum=obj.sum,
            quantity=obj.quantity,
            unitcost=obj.unitcost
        )
        .where(and_(Acthassubworks.act_id == obj.act_id, Acthassubworks.subwork_id == obj.subwork_id))
    )
    await db.commit()
    return result.rowcount

async def update_acthasfixworks_db(db: AsyncSession, obj: Acthasfixworks):
    result = await db.execute(
        update(
            Acthasfixworks
        )
        .values(
            sum=obj.sum,
            quantity=obj.quantity,
            unitcost=obj.unitcost
        )
        .where(and_(Acthasfixworks.act_id == obj.act_id, Acthasfixworks.subwork_id == obj.subwork_id))
    )
    await db.commit()
    return result.rowcount

async def select_act_doc_by_uuid(db: AsyncSession, uuid: str):
    result = await db.execute(
        select(
            Actfiles.uuid,
            Actfiles.name,
            Actfiles.num,
            Actfiles.date,
            Actfiles.extention,
            Actfiles.url,
            Actfiles.path,
            Actfiles.size,
            Actfiles.filetype,
            Actfiles.house_id,
            Actfiles.date_upload
        )
        .where(Actfiles.uuid == uuid)
    )
    return result.one_or_none()

async def select_smeta_doc_by_uuid(db: AsyncSession, uuid: str):
    result = await db.execute(
        select(
            Smetafiles.uuid,
            Smetafiles.name,
            Smetafiles.num,
            Smetafiles.date,
            Smetafiles.extention,
            Smetafiles.url,
            Smetafiles.path,
            Smetafiles.size,
            Smetafiles.filetype,
            Smetafiles.house_id,
            Smetafiles.date_upload
        )
        .where(Smetafiles.uuid == uuid)
    )
    return result.one_or_none()

async def get_year_acts_by_house_id_and_year(db: AsyncSession, year: str, house_id:int):
    result = await db.execute(
        select(
            YearActfiles
        )
        .where(and_(YearActfiles.house_id == house_id, func.extract("year", YearActfiles.date) == year.year))
    )
    return result.one_or_none()

async def get_year_acts_by_house_id(db: AsyncSession, house_id:int):
    result = await db.execute(
        select(
            YearActfiles
        ).where(YearActfiles.house_id == house_id)
    )
    return result.scalars().unique().all()

async def get_acts_by_year_and_house_id(db: AsyncSession, year: datetime, house_id: int):
    result = await db.execute(
        select(
            Acts
        )
        .where(and_(Acts.house_id == house_id, func.extract("year", Acts.date) == year.year))
    )
    return result.scalars().unique().all()

async def update_bg_task_status(db: AsyncSession, uuid: str, status: str, end_task_time: datetime):
    result = await db.execute(
        update(
            BGTasks
        )
        .values(
            status=status,
            end_datetime=end_task_time
        )
        .where(BGTasks.uuid == uuid)
    )
    await db.commit()
    return result.rowcount

async def get_bg_task_status(db: AsyncSession, uuid: str):
    result = await db.execute(
        select(
            BGTasks
        )
        .where(BGTasks.uuid == uuid)
    )
    return result.one_or_none()
