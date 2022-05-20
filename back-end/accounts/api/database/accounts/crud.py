from typing import Any, List, Optional
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import false, select, update, desc, cast, func, Integer, and_
from sqlalchemy.orm import joinedload
from datetime import datetime

from ..database import row2dict
from .models import Account, WaterCounter, GasCounter


async def get_account_data_by_account(db: AsyncSession, account: str):
    result = await db.execute(
        select(
            Account
        )
        .where(Account.account == account)
    )
    return result.scalar()

async def update_water_counter_data_by_counter_id(
    db: AsyncSession, counter_id: str, counter_data: Decimal, old_date_update: Optional[datetime], old_counter_data: Optional[Decimal], diff:Decimal
    ):
    if old_date_update:
        values ={
            'date_update': datetime.now(),
            'data': counter_data,
            'last_date_update': old_date_update,
            'old_data': old_counter_data,
            'diff': diff,
        }
    else:
        values ={
            'date_update': datetime.now(),
            'data': counter_data,
            'diff': diff,
        }

    await db.execute(
        update(WaterCounter)
        .where(WaterCounter.id == int(counter_id))
        .values(**values)
    )
    await db.commit()

async def update_gas_counter_data_by_counter_id(
    db: AsyncSession, counter_id: str, counter_data: Decimal, old_date_update: Optional[datetime], old_counter_data: Optional[Decimal], diff:Decimal
    ):
    if old_date_update:
        values ={
            'date_update': datetime.now(),
            'data': counter_data,
            'last_date_update': old_date_update,
            'old_data': old_counter_data,
            'diff': diff,
        }
    else:
        values ={
            'date_update': datetime.now(),
            'data': counter_data,
            'diff': diff,
        }

    await db.execute(
        update(GasCounter)
        .where(GasCounter.id == int(counter_id))
        .values(**values)
    )
    await db.commit()    
