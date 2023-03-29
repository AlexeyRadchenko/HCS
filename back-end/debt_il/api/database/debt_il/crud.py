from typing import Any, List, Optional
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import false, select, update, desc, cast, func, Integer, and_, insert, or_
from sqlalchemy.orm import joinedload, selectinload, join, contains_eager
from datetime import datetime

from ..database import row2dict
from .models import All_il, Accounts_il, Egrn_il, Payments_il, Passport_il, IL_accounts, Organisations_il

async def create_debt_il_list_with_accounts(db: AsyncSession, data: Any, files: dict):
    period = [datetime.strptime(p, '%Y-%m-%d') for p in data['period'] if p != '']
    accounts_created_objs = []
    for account in data['accounts_il']:
        pasp = account['passport_il']
        passport_db_object = Passport_il(
            serial=pasp['seria'],
            number=pasp['number'],
            who_take=pasp['who_take'],
            date_take=datetime.strptime(pasp['when_take'], '%Y-%m-%d') if pasp['when_take'] else None,
            squad_code=pasp['squad_code'],
            birth_date=datetime.strptime(pasp['birth_date'], '%Y-%m-%d') if pasp['birth_date'] else None,
            birth_place=pasp['birth_place'],
            scan=pasp['scan']                     
        )
        db.add(passport_db_object)
        await db.commit()
        await db.refresh(passport_db_object)
        acc = Accounts_il(
            account_number=account['account_number'],
            name=account['name'],
            second_name=account['second_name'],
            surname=account['surname'],
            inn=account['inn'],
            passport=passport_db_object.id
        )
        db.add(acc)
        await db.commit()
        await db.refresh(acc)
        accounts_created_objs.append(acc.uuid)
        account['uuid'] = acc.uuid

    IL_list_db_object = All_il(
        street=data['street'],
        house=data['house'],
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
        organisation_id=data['uk_org'],
    )

    db.add(IL_list_db_object)
    await db.commit()
    await db.refresh(IL_list_db_object)

    for acc_uuid in accounts_created_objs:
        create_relation_il_accounts_obj = IL_accounts (
            il_id=IL_list_db_object.id,
            account_uuid=acc_uuid
        )
        db.add(create_relation_il_accounts_obj)
        await db.commit()
        data['id'] = IL_list_db_object.id
    return data

async def update_debt_il_list_with_accounts(db: AsyncSession, data: Any, files: dict):
    period = [datetime.strptime(p, '%Y-%m-%d') for p in data['period'] if p != '' and p != ',']
    accounts_created_objs = []
    for account in data['accounts_il']:
        pasp_resulti_in_db = None
        pasp = account['passport_il']
        if not pasp.get('empty'):
            pasp_in_db = await db.execute(
                select(
                    Passport_il
                )
                .where(Passport_il.id == pasp['id'])
            )
            pasp_resulti_in_db = pasp_in_db.scalars()
            if pasp_resulti_in_db:
                await db.execute(
                    update(Passport_il)\
                    .where(Passport_il.id == pasp['id'])\
                    .values(
                        serial=pasp['seria'],
                        number=pasp['number'],
                        who_take=pasp['who_take'],
                        date_take=datetime.strptime(pasp['when_take'], '%Y-%m-%d') if pasp['when_take'] else None,
                        squad_code=pasp['squad_code'],
                        birth_date=datetime.strptime(pasp['birth_date'], '%Y-%m-%d') if pasp['birth_date'] else None,
                        birth_place=pasp['birth_place'],
                        scan=pasp['scan']  
                    )
                )    
                await db.commit()                     
       
        await db.execute(
            update(Accounts_il)\
            .where(Accounts_il.uuid == account['uuid'])\
            .values(
                account_number=account['account_number'],
                name=account['name'],
                second_name=account['second_name'],
                surname=account['surname'],
                inn=account['inn'],
                passport=pasp_resulti_in_db.id if pasp_resulti_in_db else None
            )
        )    
        await db.commit()

    await db.execute(
        update(All_il)\
        .where(All_il.id == data['id'])\
        .values(
            street=data['street'],
            house=data['house'],
            appartment=data['appartment'],
            one_or_parts=data['one_or_parts'],
            property_self=data['property_self'],
            il_number=data['il_number'],
            il_date=datetime.strptime(data['il_date'][:9], '%Y-%m-%d'),
            gov_tax=data['gov_tax'],
            debt_sum_il=data['debt_sum_il'],
            start_exec_pross_date=data['period'][0] if len(period) == 2 else None,
            end_exec_pross_date=data['period'][1] if len(period) == 2 else None,
            notes='',
            organisation_id=data['uk_org'],
        )
    )    
    await db.commit()

    return data

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

async def create_debt_il_object(db:AsyncSession, obj:Any):
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj
    
    
