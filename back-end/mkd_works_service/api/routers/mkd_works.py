from fastapi import APIRouter, Depends, Security, UploadFile, Form
from sqlalchemy.ext.asyncio.session import AsyncSession
from typing import List, Annotated
from datetime import datetime
from os import path

from ..database.mkd_works.schemas import HousesMKDSchema, ActFilesSchema
from ..database.mkd_works.crud import get_all_houses, get_all_mkd_works_by_house_id, get_furure_work_id_from_db
from api.security.acess_depends import user_scope_authorize
from ..database.database import get_async_session
from api.settings.settings import settings
from ..utils.utils import chunked_copy



router = APIRouter()


@router.get("/houses/all", response_model=list[HousesMKDSchema])
async def get_mkd_works_all_handler(
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.MANAGEMENT_MKD_WORKS_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session)
    ):

    houses_in_db = await get_all_houses(db_session)    
    return houses_in_db

@router.get("/houses/works/all/{house_id}", response_model=list[ActFilesSchema])
async def get_mkd_works_all_by_house_id(
    house_id: int,
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.MANAGEMENT_MKD_WORKS_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session)
    ):
    all_works_by_house_id = await get_all_mkd_works_by_house_id(db_session, house_id)
    return all_works_by_house_id

@router.get("/houses/works/future_id/{house_id}")
async def get_future_work_id(
    house_id: int,
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.MANAGEMENT_MKD_WORKS_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session)
    ):
    work = await get_furure_work_id_from_db(db_session, house_id)
    if work:
        return {
            'future_work_id': work.id + 1
        }
    else:
        return {
            'future_work_id': 1
        }

@router.post("/uploadfile/act")
async def create_upload_act_file(
    actnum: Annotated[str, Form()],
    actdate: Annotated[datetime, Form()],
    workid: Annotated[str, Form()],
    file: UploadFile | None = None,
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.MANAGEMENT_MKD_WORKS_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session)
    ):
    if not file:
        return {"message": "No file sent"}
    else:
        if settings.FILE_SERVER == 'localhost':
            url = '/download/act/'
        else:
            url = f'https://{settings.FILE_SERVER}:{settings.FILE_SERVER_PORT}/download/act'

        if workid == 'undefined':
            print("not exist", workid)
            #initiate act object new and get id    
        else:
            print("exist", workid)
            #create act document with ref to act.id=workid
        fullpath = path.join(settings.ACT_FILES_STORE_PATH, file.filename)
        await chunked_copy(file, fullpath)
        return {
            "filename": file.filename,
            "actdate": actdate,
            "actnum": actnum,
            "url": url,
            "workid": workid, #send work id from db object
            }
    