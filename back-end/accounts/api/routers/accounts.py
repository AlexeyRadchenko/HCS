from fastapi import APIRouter, Depends, Security
from sqlalchemy.ext.asyncio.session import AsyncSession

from ..database.accounts.schemas import AccountSchema, AccountWaterCounterSchema
from ..database.database import get_async_session
from ..database.accounts.crud import (
    get_account_data_by_account, update_water_counter_data_by_counter_id, update_gas_counter_data_by_counter_id,
     update_electric_counter_data_by_counter_id
     )
from ..security.access_depends import user_scope_authorize
from ..utils.validators import valid_counter_data, valid_data_date, valid_counter_electric_data
from .depends import counter_data_form_depend, counter_electric_data_form_depend
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
async def insert_counter_water_data_handler(
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
async def insert_counter_gas_data_handler(
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

@router.put("/account/{account}/update_electric_counter_data")
async def insert_counter_electric_data_handler(
    account: str,
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.ACCOUNT_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session),
    form_data: dict = Depends(counter_electric_data_form_depend)
    ):
    valid_old_date, old_date = valid_data_date(form_data['old_date_update'])
    valid_old_simple, old_simple_data = valid_counter_electric_data(form_data['old_counter_simple_data'])
    valid_old_day, old_day_data = valid_counter_electric_data(form_data['old_counter_day_data'])
    valid_old_night, old_night_data = valid_counter_electric_data(form_data['old_counter_night_data'])
    valid_simple, simple_data = valid_counter_electric_data(form_data['counter_simple_data'])
    valid_day, day_data = valid_counter_electric_data(form_data['counter_day_data'])
    valid_night, night_data = valid_counter_electric_data(form_data['counter_night_data'])
    if not valid_simple and (not valid_day or not valid_night):
        return {"status": "error", "difference": 0, "message": "Введите целое число. Например 15100"}
    if valid_old_simple:
        if (old_simple_data > simple_data):
            return {"status": "error", "difference": 0, "message": "Введите показания больше предыдущих !"}
        simple_diff = simple_data - old_simple_data
        day_diff, night_diff = None, None 
    if valid_old_day and valid_old_night:
        if (old_day_data > day_data) or (old_night_data > night_data):
            return {"status": "error", "difference": 0, "message": "Введите показания больше предыдущих !"}
        day_diff = day_data - old_day_data
        night_diff = night_data - old_night_data
        simple_diff = None
    await update_electric_counter_data_by_counter_id(
        db_session, form_data['counter_id'], form_data['type'], old_date, simple_data, day_data, night_data,  old_simple_data,
        old_day_data, old_night_data, simple_diff, day_diff, night_diff)
    return {"status": "OK",
     "simple_difference": simple_diff, "day_difference": day_diff, "night_difference": night_diff, "message": "Показания счетчика записаны", "exch": valid_old_date}  
