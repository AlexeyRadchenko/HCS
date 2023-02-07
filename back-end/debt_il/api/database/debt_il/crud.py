from typing import Any, List, Optional
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import false, select, update, desc, cast, func, Integer, and_
from sqlalchemy.orm import joinedload
from datetime import datetime

from ..database import row2dict
from .models import All_il, Accounts_il, Egrn_il

async def create_debt_il_object(db: AsyncSession, debt_il_object: Any):
    db.add(debt_il_object)
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

async def create_debt_il_egrn_doc_object(db: AsyncSession, debt_il_egrn_doc_object: Any):
    db.add(debt_il_egrn_doc_object)
    await db.commit()
    await db.refresh(debt_il_egrn_doc_object)
    return debt_il_egrn_doc_object

async def get_debt_il_egrn_docs_by_il_id(db: AsyncSession, il_id: int):
    result = await db.execute(
        select(
            Egrn_il
        ).where(and_(Egrn_il.del_mark == False, Egrn_il.il_id == il_id))
    )
    return result.scalars().unique().all()

async def update_debt_il_egrn_doc_object(db: AsyncSession, debt_il_egrn_doc_object: Any):
    await db.execute(
        update(Egrn_il)
        .where(Egrn_il.il_id == debt_il_egrn_doc_object.il_id)
        .values(
            date=debt_il_egrn_doc_object.date,
            number=debt_il_egrn_doc_object.number,
            file=debt_il_egrn_doc_object.file,
            note=debt_il_egrn_doc_object.note,
            del_mark=debt_il_egrn_doc_object.del_mark
        )
    )
    await db.commit()
    return debt_il_egrn_doc_object

async def del_egrn_doc_by_id(db: AsyncSession, egrn_doc_id: int):
    await db.execute(
        update(Egrn_il)
        .where(Egrn_il.id == egrn_doc_id)
        .values(
            del_mark=True
        )
    )
    await db.commit()
    return True

async def get_il_list_by_il_number(db: AsyncSession, il_number: str):
    result = await db.execute(
        select(
            All_il
        )
        .options(
            joinedload(All_il.accounts_il)
        )
        .where(and_(All_il.del_mark == False, All_il.il_number == il_number))
    )
    return result.scalars().unique().all()