from typing import Any, List, Optional
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import false, select, update, desc, cast, func, Integer, and_
from sqlalchemy.orm import joinedload
from datetime import datetime

from ..database import row2dict
from .models import All_il

async def get_all_il_data_list(db: AsyncSession):
    result = await db.execute(
        select(
            All_il
        )
    )
    return result.scalars().unique().all()