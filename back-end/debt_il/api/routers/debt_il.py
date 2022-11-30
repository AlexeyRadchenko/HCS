from fastapi import APIRouter, Depends, Security, UploadFile, File
from sqlalchemy.ext.asyncio.session import AsyncSession
from typing import List

from ..database.debt_il.schemas import AllILDataSchema, AccountILSchema
from ..database.debt_il.crud import get_all_il_data_list, get_all_fio_from_db
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

@router.get("/il/accounts/all/data", response_model=List[AccountILSchema])
async def get_accounts_debt_il_handler(
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.MANAGEMENT_DEBT_IL_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session)
    ):
    accounts_data_in_db = await get_all_fio_from_db(db_session)
    return accounts_data_in_db

@router.post("/il/upload/payments_il")
async def upload(
    file: UploadFile = File(...),
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.MANAGEMENT_DEBT_IL_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session)
    ):

    try:
        with open(settings.DEBT_IL_UPLOAD_PATH + '/' + file.filename, 'wb') as f:
            contents = 1
            while contents:
                contents = file.file.read(1024 * 1024)
                f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file(s)"}
    finally:
        file.file.close()
            
    return {"message": f"Successfuly uploaded {file.filename}", "fPath": settings.DEBT_IL_UPLOAD_PATH + '/' + file.filename}   

