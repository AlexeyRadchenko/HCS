from fastapi import APIRouter, Depends, Security, UploadFile, Form
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio.session import AsyncSession
from typing import List, Annotated
from datetime import datetime, timezone
from os import path

from ..database.mkd_works.schemas import HousesMKDSchema, DoneWorksSchema, ReferenceBookSchema, WorkEditSchema
from ..database.mkd_works.crud import (
    get_all_houses, get_all_mkd_works_by_house_id, get_furure_work_id_from_db, create_mkd_works_db_object, get_all_mainworks,
    get_all_subworks, get_all_fixworks
    )
from ..database.mkd_works.models import Acts, Actfiles, Actshasactfiles, Smetafiles, Actshassmetafiles
from api.security.acess_depends import user_scope_authorize
from ..database.database import get_async_session
from api.settings.settings import settings
from ..utils.utils import chunked_copy, get_file_extension



router = APIRouter()


@router.get("/houses/all", response_model=list[HousesMKDSchema])
async def get_mkd_works_all_handler(
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.MANAGEMENT_MKD_WORKS_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session)
    ):

    houses_in_db = await get_all_houses(db_session)    
    return houses_in_db

@router.get("/houses/works/all/{house_id}", response_model=list[DoneWorksSchema])
async def get_mkd_works_all_by_house_id(
    house_id: int,
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.MANAGEMENT_MKD_WORKS_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session)
    ):
    all_works_by_house_id = await get_all_mkd_works_by_house_id(db_session, house_id)
    #print(">>>>>>>>>>>>>>>>>>>>>>", all_works_by_house_id[0])
    #print(">>>>>>>>>>>>>>>>>>>>>>", all_works_by_house_id[0].subworks)
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
    houseid: Annotated[int, Form()],
    workid: Annotated[str, Form()],
    actnum: Annotated[str | None, Form()] = None,
    actdate: Annotated[datetime | None, Form()] = None,
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
            url = f'https://{settings.FILE_SERVER}:{settings.FILE_SERVER_PORT}/download/act/'
        timstamp1 =int(datetime.now(tz=timezone.utc).timestamp() * 1000)  
        fullpath = path.join(settings.ACT_FILES_STORE_PATH, f'{str(timstamp1)}_{file.filename}')
        actfile = Actfiles(
                name=file.filename,
                date=actdate,
                num=actnum,
                extention=get_file_extension(file.filename),
                url=url,
                path=fullpath,
                size=str(file.size),
                filetype=file.content_type,  # assuming the file type is correct in this case
                house_id=houseid,
            )
        cr_act_doc = await create_mkd_works_db_object(db_session, actfile)
        
        if workid == 'undefined':
            #print("not exist", workid)
            act = Acts(
                house_id=houseid,
                all_sum='0',
            )
            cr_work = await create_mkd_works_db_object(db_session, act)
            acthasactfiles = Actshasactfiles(
                act_id=cr_work.id,
                actfile_uuid=cr_act_doc.uuid
            )
            workid=cr_work.id
        else:
            #print("exist", workid)
            #create act document with ref to act.id=workid
            acthasactfiles = Actshasactfiles(
                act_id=int(workid),
                actfile_uuid=cr_act_doc.uuid
            )          
        await chunked_copy(file, fullpath)
        ref_obj = await create_mkd_works_db_object(db_session, acthasactfiles)
        return {
            "filename": file.filename,
            "actdate": actdate,
            "actnum": actnum,
            "url": url,
            "workid": int(workid), #send work id from db object
            }
    
@router.post("/uploadfile/smeta")
async def create_upload_smeta_file(
    houseid: Annotated[int, Form()],
    workid: Annotated[str, Form()],
    smetanum: Annotated[str | None, Form()] = None,
    smetadate: Annotated[datetime | None, Form()] = None,
    file: UploadFile | None = None,
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.MANAGEMENT_MKD_WORKS_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session)
    ):
    if not file:
        return {"message": "No file sent"}
    else:
        if settings.FILE_SERVER == 'localhost':
            url = '/download/smeta/'
        else:
            url = f'https://{settings.FILE_SERVER}:{settings.FILE_SERVER_PORT}/download/smeta/'   
        timstamp2 =int(datetime.now(tz=timezone.utc).timestamp() * 1000)  
        fullpathsmeta = path.join(settings.SMETA_FILES_STORE_PATH, f'{str(timstamp2)}_{file.filename}')
        smetafile = Smetafiles(
                name=file.filename,
                date=smetadate,
                num=smetanum,
                extention=get_file_extension(file.filename),
                url=url,
                path=fullpathsmeta,
                size=str(file.size),
                filetype=file.content_type,  # assuming the file type is correct in this case
                house_id=houseid,
            )
        cr_smeta_doc = await create_mkd_works_db_object(db_session, smetafile)

        if workid == 'undefined':
            #print("not exist", workid)
            act = Acts(
                house_id=houseid,
                all_sum='0',
            )
            cr_work = await create_mkd_works_db_object(db_session, act)
            acthassmetafiles = Actshassmetafiles(
                act_id=cr_work.id,
                smetafile_uuid=cr_smeta_doc.uuid
            )
            workid=cr_work.id
        else:
            #print("exist", workid)
            #create act document with ref to act.id=workid
            acthassmetafiles = Actshassmetafiles(
                act_id=int(workid),
                smetafile_uuid=cr_smeta_doc.uuid
            )            
        await chunked_copy(file, fullpathsmeta)
        ref_obj = await create_mkd_works_db_object(db_session, acthassmetafiles)
        return {
            "filename": file.filename,
            "smetadate": smetadate,
            "smetanum": smetanum,
            "url": url,
            "workid": int(workid), #send work id from db object
            }    

@router.get("/get_reference_book_data/all")
async def get_reference_book_data_all(
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.MANAGEMENT_MKD_WORKS_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session)
    ):
    mainworks = await get_all_mainworks(db_session)
    subworks = await get_all_subworks(db_session)
    fixworks = await get_all_fixworks(db_session)
    reference_book_schema_obj = ReferenceBookSchema(
        mainworks=mainworks,
        subworks=subworks,
        fixworks=fixworks
    )
    
    return JSONResponse(content=reference_book_schema_obj.model_dump())

@router.post("/houses/works/edit/")
async def update_act_model(
    work: WorkEditSchema,
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.MANAGEMENT_MKD_WORKS_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session)
    ):
    act_edit_model_object = Acts(
        id=int(work.id),
        num=work.num,
        all_sum=work.all_sum,
        month_year_works=work.month_year_works,
        house_id=work.house_id,
    )
    print("----------------->", work.works)
    print("----------------->", work.mainworks)
    print("----------------->", work.subworks)
    return