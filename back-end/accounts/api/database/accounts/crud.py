from typing import Any, List, Optional
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import false, select, update, desc, cast, func, Integer, and_
from sqlalchemy.orm import joinedload
from datetime import datetime

from ..database import row2dict
from .models import Account, ElectricCounter, WaterCounter, GasCounter


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

async def update_electric_counter_data_by_counter_id(
    db: AsyncSession, counter_id: str, type: str,  old_date_update: Optional[datetime], simple_data: Optional[int], day_data: Optional[int],
    night_data: Optional[int], old_simple_data: Optional[int], old_day_data: Optional[int], old_night_data: Optional[int],
    simple_diff:Optional[int], day_diff:Optional[int], night_diff:Optional[int]
    ):

    if old_date_update:
        if type == 'single':
            values ={
                'date_update': datetime.now(),
                'simple_data': simple_data,
                'last_date_update': old_date_update,
                'old_simple_data': old_simple_data,
                'diff': simple_diff,
            }
        else:
            values ={
                'date_update': datetime.now(),
                'day_data': simple_data,
                'night_data': night_data,
                'last_date_update': old_date_update,
                'old_day_data': old_day_data,
                'old_night_data': old_night_data,
                'day_diff': day_diff,
                'night_diff': night_diff,
            }    
    else:
        if type =='single':
            values ={
                'date_update': datetime.now(),
                'simple_data': simple_data,
                'simple_diff': simple_diff,
            }
        else:
            values ={
                'date_update': datetime.now(),
                'day_data': day_data,
                'night_data': night_data,
                'day_diff': day_diff,
                'night_diff': night_diff,
            }

    await db.execute(
        update(ElectricCounter)
        .where(ElectricCounter.id == int(counter_id))
        .values(**values)
    )
    await db.commit()    
