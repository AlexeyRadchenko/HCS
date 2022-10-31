from fastapi import APIRouter, Depends, Security
from sqlalchemy.ext.asyncio.session import AsyncSession
from typing import List

from ..database.debt_il.schemas import AllILDataSchema
from ..database.debt_il.crud import get_all_il_data_list
from ..security.access_depends import user_scope_authorize
from ..database.database import get_async_session
from ..settings.settings import settings


router = APIRouter()


@router.get("/il/all/data", response_model=List[AllILDataSchema])
async def create_contact_address_handler(
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.MANAGEMENT_DEBT_IL_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session)
    ):
    il_data_in_db = await get_all_il_data_list(db_session)
    return il_data_in_db