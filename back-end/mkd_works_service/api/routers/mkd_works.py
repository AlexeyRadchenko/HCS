from fastapi import APIRouter, Depends, Security
from sqlalchemy.ext.asyncio.session import AsyncSession
from typing import List

from ..database.mkd_works.schemas import HousesMKDSchema
from ..database.mkd_works.crud import get_all_houses
from api.security.acess_depends import user_scope_authorize
from ..database.database import get_async_session
from api.settings.settings import settings



router = APIRouter()


@router.get("/houses/all", response_model=list[HousesMKDSchema])
async def get_mkd_works_all_handler(
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.MANAGEMENT_MKD_WORKS_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session)
    ):

    houses_in_db = await get_all_houses(db_session)
    
    return houses_in_db