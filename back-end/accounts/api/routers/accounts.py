from fastapi import APIRouter, Depends, Security
from sqlalchemy.ext.asyncio.session import AsyncSession

from ..database.accounts.schemas import AccountSchema, AccountWaterCounterSchema
from ..database.database import get_async_session
from ..database.accounts.crud import get_account_data_by_account, update_water_counter_data_by_counter_id, update_gas_counter_data_by_counter_id
from ..security.access_depends import user_scope_authorize
from ..utils.validators import valid_counter_data, valid_data_date
from .depends import counter_data_form_depend
from ..settings.settings import settings

router = APIRouter()


@router.get("/account/{account}/data", response_model=AccountSchema)
async def create_contact_address_handler(
    account: str,
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.ACCOUNT_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session)
    ):
    account_data_in_db = await get_account_data_by_account(db_session, account)
    return account_data_in_db

@router.put("/account/{account}/update_water_counter_data")
async def insert_counter_data_handler(
    account: str,
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.ACCOUNT_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session),
    form_data: dict = Depends(counter_data_form_depend)
    ):
    valid_old_date, old_date = valid_data_date(form_data['old_date_update'])
    _, old_data = valid_counter_data(form_data['old_counter_data'])
    valid_data, data = valid_counter_data(form_data['counter_data'])
    if not valid_data:
        return {"status": "error", "difference": 0, "message": "Введите число разделенные точкой (0.0)"}
    if  (old_data > data):
            return {"status": "error", "difference": 0, "message": "Введите показания больше предыдущих !"}
    diff = data - old_data
    await update_water_counter_data_by_counter_id(db_session, form_data['counter_id'], data, old_date, old_data, diff)
    return {"status": "OK", "difference": diff, "message": "Показания счетчика записаны", "exch": valid_old_date}

@router.put("/account/{account}/update_gas_counter_data")
async def insert_counter_data_handler(
    account: str,
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.ACCOUNT_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session),
    form_data: dict = Depends(counter_data_form_depend)
    ):
    valid_old_date, old_date = valid_data_date(form_data['old_date_update'])
    _, old_data = valid_counter_data(form_data['old_counter_data'])
    valid_data, data = valid_counter_data(form_data['counter_data'])
    if not valid_data:
        return {"status": "error", "difference": 0, "message": "Введите число разделенные точкой (0.0)"}
    if  (old_data > data):
            return {"status": "error", "difference": 0, "message": "Введите показания больше предыдущих !"}
    diff = data - old_data
    await update_gas_counter_data_by_counter_id(db_session, form_data['counter_id'], data, old_date, old_data, diff)
    return {"status": "OK", "difference": diff, "message": "Показания счетчика записаны", "exch": valid_old_date}    
