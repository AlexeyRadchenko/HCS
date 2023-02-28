from typing import Any, List, Optional
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import false, select, update, desc, cast, func, Integer, and_, insert, or_
from sqlalchemy.orm import joinedload, selectinload, join, contains_eager
from datetime import datetime

from ..database import row2dict
from .models import All_il, Accounts_il, Egrn_il, Payments_il, Passport_il, IL_accounts

async def create_debt_il_list_with_accounts(db: AsyncSession, data: Any, files: dict):
    period = [datetime.strptime(p, '%Y-%m-%d') for p in data['period'] if p != '']
    accounts_created_objs = []
    for account in data['accounts_il']:
        pasp = account['passport_il']
        passport_db_object = Passport_il(
            seria=pasp['seria'],
            number=pasp['number'],
            who_take=pasp['who_take'],
            when_take=datetime.strptime(pasp['when_take'], '%Y-%m-%d'),
            squad_code=pasp['squad_code'],
            birth_date=pasp['birth_date'],
            birth_place=pasp['birth_place'],
            scan=files[pasp['uploadFiles'][1]] if len(pasp['uploadFiles'] == 2) else ''                       
        )
        await db.add(passport_db_object)
        await db.commit()
        await db.refresh(passport_db_object)
        acc = Accounts_il(
            account_number=account['account_number'],
            name=account['account_number'],
            second_=account['second_number'],
            surname=account['account_surname'],
            inn=account['inn'],
            passport=passport_db_object.id
        )
        await db.add(acc)
        await db.commit()
        await db.refresh(acc)
        accounts_created_objs.append(acc.id)

    IL_list_db_object = All_il(
        street=data['street'],
        house=data['home'],
        appartment=data['appartment'],
        one_or_parts=data['one_or_parts'],
        property_self=data['property_self'],
        il_number=data['il_number'],
        il_date=datetime.strptime(data['il_date'], '%Y-%m-%d'),
        gov_tax=data['gov_tax'],
        debt_sum_il=data['debt_sum_il'],
        start_exec_pross_date=data['period'][0] if len(period) == 2 else None,
        end_exec_pross_date=data['period'][1] if len(period) == 2 else None,
        notes='',
        organistion_id=1,
    )

    await db.add(IL_list_db_object)
    await db.commit()
    await db.refresh(IL_list_db_object)

    for acc_id in accounts_created_objs:
        create_relation_il_accounts_obj = IL_accounts (
            il_id=IL_list_db_object.id,
            account_uuid=acc_id
        )
        await db.add(create_relation_il_accounts_obj)
        await db.commit()
    return 

async def get_all_il_data_list(db: AsyncSession):
    result = await db.execute(
        select(
            All_il
        )
        .options(joinedload(All_il.payments_il))
        .where(All_il.del_mark == False)
    )
    return result.scalars().unique().all()

async def get_all_il_data_list_by_edge_date(db: AsyncSession, edge_date:datetime):
    result = await db.execute(
        select(
            All_il
        )
        .options(joinedload(All_il.payments_il.and_(Payments_il.date <= edge_date)))
        .where(All_il.del_mark == False)   
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

async def create_payment_record_in_db(
    db: AsyncSession, date: datetime, type: str, sum: Decimal, il_id: int, uuid: Optional[str]=None, fio: Optional[str]=None):
    await db.execute(
        insert(Payments_il)
        .values(
            date=date,
            type=type,
            sum=sum,
            who_paid_uuid=uuid,
            notes=fio,
            il_id=il_id
        )
    )
    await db.commit()

async def get_payments_history_by_il_id(db: AsyncSession, il_id: int):
    result = await db.execute(
        select(
            Payments_il
        )
        .options(
            joinedload(Payments_il.account_il)
        )
        .where(
            Payments_il.il_id == il_id 
        )
    )
    return result.scalars().unique().all()