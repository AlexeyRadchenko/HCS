from fastapi import APIRouter, Depends, Security, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.ext.asyncio.session import AsyncSession
from typing import List, Optional
from datetime import datetime

from ..database.debt_il.schemas import ( AllILDataSchema, AccountILSchema, EgrnILSchema, EGRNDocFileSchema, PaymentUploadDataListSchema, 
    PaymentsILSchema
 )
from ..database.debt_il.crud import (
    get_all_il_data_list, get_all_fio_from_db, get_debt_il_egrn_docs_by_il_id, create_debt_il_egrn_doc_object, del_egrn_doc_by_id,
    get_il_list_by_il_number, create_payment_record_in_db, get_payments_history_by_il_id, get_all_il_data_list_by_edge_date
    )
from ..database.debt_il.models import Egrn_il, Payments_il
from ..security.access_depends import user_scope_authorize
from ..database.database import get_async_session
from ..settings.settings import settings
from ..utils.utils import get_payer_uuid_or_fio, get_date_from_str, get_decimal_from_str

router = APIRouter()


@router.get("/il/all/data", response_model=List[AllILDataSchema])
async def create_contact_address_handler(
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.MANAGEMENT_DEBT_IL_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session)
    ):
    il_data_in_db = await get_all_il_data_list(db_session)
    return il_data_in_db

@router.get("/il/{month_year}/data", response_model=List[AllILDataSchema])
async def create_contact_address_handler(
    month_year: str,
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.MANAGEMENT_DEBT_IL_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session)
    ):
    edge_date = datetime.strptime(month_year, '%Y-%m-%d')
    il_data_in_db = await get_all_il_data_list_by_edge_date(db_session, edge_date)
    return il_data_in_db 

@router.post("/il/all/create")
async def create_il_list_with_accounts(
    egrnDocDate: Optional[str] = Form(None),
    egrnDocNumber:Optional[str] = Form(None),
    egrnDocNote: Optional[str] = Form(None),
    il_number:Optional[str] = Form(None),
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.MANAGEMENT_DEBT_IL_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session)
    ):
    pass

@router.get("/il/accounts/all/data", response_model=List[AccountILSchema])
async def get_accounts_debt_il_handler(
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.MANAGEMENT_DEBT_IL_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session)
    ):
    accounts_data_in_db = await get_all_fio_from_db(db_session)
    return accounts_data_in_db

@router.post("/il/upload/{storage_path}")
async def upload(
    storage_path: str,
    egrnDocDate: Optional[str] = Form(None),
    egrnDocNumber:Optional[str] = Form(None),
    egrnDocNote: Optional[str] = Form(None),
    il_number:Optional[str] = Form(None),
    il_base_id:str = Form(...),
    file: UploadFile = File(...),
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.MANAGEMENT_DEBT_IL_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session)
    ):
    path_file=None
    if storage_path == 'payments_il':
        path_file = settings.DEBT_IL_UPLOAD_PATH + '/' + file.filename
    elif storage_path == 'egrn_il':
        path_file = settings.FILE_STORAGE_PATH + '/egrn/' + str(int(datetime.utcnow().timestamp())) + '__' + il_base_id + '_'  +  file.filename    
        
    try:
        with open(path_file, 'wb') as f:
            contents = 1
            while contents:
                contents = file.file.read(1024 * 1024)
                f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file(s)"}
    finally:
        file.file.close()

    if storage_path == 'egrn_il':
        egrn_doc_date_datetime = None
        if egrnDocDate:
            egrn_doc_date_datetime = datetime.strptime(egrnDocDate, '%Y-%m-%d')
        egrn_doc_base_object = Egrn_il(
            date=egrn_doc_date_datetime, number=egrnDocNumber, note=egrnDocNote, file=path_file, del_mark=False, il_id=int(il_base_id), name=file.filename
            )
        created_egrn_doc = await create_debt_il_egrn_doc_object(db_session, egrn_doc_base_object) 
        egrn_doc_val_model = EgrnILSchema().from_orm(created_egrn_doc)
        return egrn_doc_val_model.json()        
    else:
        return {"message": f"Successfuly uploaded {file.filename}", "fPath": settings.DEBT_IL_UPLOAD_PATH + '/' + file.filename}

@router.delete("/il/egrn_il_doc/data/{egrn_doc_id}")
async def delete_egrn_doc_by_id(
    egrn_doc_id: str,
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.MANAGEMENT_DEBT_IL_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session)
    ):
    bool_result = await del_egrn_doc_by_id(db_session, int(egrn_doc_id))
    if bool_result:
        return {"result": "success"}
    else:
        return {"result": "error"}


@router.get("/il/egrn_il_doc/data/{il_id}", response_model=List[EgrnILSchema])
async def get_egrn_il_docs_data_by_il_id(
    il_id: str,
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.MANAGEMENT_DEBT_IL_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session)
    ):
    egrn_data_list = await get_debt_il_egrn_docs_by_il_id(db_session, int(il_id))
    return egrn_data_list

@router.post("/il/egrn_il_doc/download/")
async def get_egrn_doc_by_file_path(
    file: EGRNDocFileSchema,
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.MANAGEMENT_DEBT_IL_SCOPE]),
    ):
    return FileResponse(path=file.file_path)

@router.post("/il/payment_il_doc/data/upload")
async def upload_payment_doc_data(
    data: PaymentUploadDataListSchema,   
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.MANAGEMENT_DEBT_IL_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session)
):  
    broken_data = []
    data_dict = data.dict()
    for data_row in data_dict['data']:
        il_list = await get_il_list_by_il_number(db_session, data_row['il'])
        if not il_list:
            broken_data.append(data_row)
            continue
        date = await get_date_from_str(data_row['date'])
        sum = await get_decimal_from_str(data_row['sum'])
        uuid, fio = await get_payer_uuid_or_fio(il_list[0].accounts_il, data_row['account_name'])
        if uuid:
            await create_payment_record_in_db(
                db_session, date, data_row['type'], sum, il_list[0].id, uuid=uuid)
        else:
            await create_payment_record_in_db(
                db_session, date, data_row['type'], sum, il_list[0].id, fio=fio)
            
    return JSONResponse(content=broken_data)

@router.get("/il/payments_il_doc/data/{il_id}", response_model=List[PaymentsILSchema])
async def get_payments_il_data_by_il_id(
    il_id: str,
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.MANAGEMENT_DEBT_IL_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session)
    ):
    payments_history_in_db = await get_payments_history_by_il_id(db_session, int(il_id))
    return payments_history_in_db
