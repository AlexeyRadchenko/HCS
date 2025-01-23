from fastapi import APIRouter, Depends, Security, UploadFile, Form, BackgroundTasks
from fastapi.responses import JSONResponse, FileResponse
from sqlalchemy.ext.asyncio.session import AsyncSession
from typing import List, Annotated
from datetime import datetime, timezone
from os import path

from ..database.mkd_works.schemas import (HousesMKDSchema, DoneWorksSchema, ReferenceBookSchema, WorkEditSchema, WorkNewSchema, YearActFilesSchema, 
    BGTaskSchema, TechFilesSchema)
from ..database.mkd_works.crud import (
    get_all_houses, get_all_mkd_works_by_house_id, get_furure_work_id_from_db, create_mkd_works_db_object, get_all_mainworks,
    get_all_subworks, get_all_fixworks, update_act_db, update_acthasfixworks_db, update_acthassubworks_db, select_act_doc_by_uuid,
    select_smeta_doc_by_uuid, get_year_acts_by_house_id, get_acts_by_year_and_house_id, get_year_acts_by_house_id_and_year, get_bg_task_status,
    get_year_acts_file_by_year_act_uuid, get_techdoc_file_by_uuid, get_tech_files_by_house_id, delete_act_old_works
    )
from ..database.mkd_works.models import (Acts, Actfiles, Actshasactfiles, Smetafiles, Actshassmetafiles, Acthassubworks, Acthasfixworks, BGTasks,
    Techfiles)
from api.security.acess_depends import user_scope_authorize
from ..database.database import get_async_session
from api.settings.settings import settings
from ..utils.utils import chunked_copy, get_file_extension, calcSum, getWorkSubId
from ..tasks.tasks import genereate_year_act_xlsx_file



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
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>WORKS", work.works)
    res = None
    if len(work.subworks) > 0:
        res = await delete_act_old_works(db_session, int(work.id), 'subworks')
    if len(work.fixworks) > 0:
        res = await delete_act_old_works(db_session, int(work.id), 'fixworks')
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>WORKS", res)    
    act_edit_model_object = Acts(
        id=int(work.id),
        num=work.num,
        all_sum=work.all_sum,
        month_year_works=work.month_year_works,
        house_id=int(work.house_id),
        director=work.directorSovietFIO,
        director_appartment=work.directorAppartNum
    )
    sum = 0
    if len(work.works) > 0:
        for s in work.works:
            sum = calcSum(s.sum, sum=sum)
            if s.workType == 'subwork':
                act_subwork = Acthassubworks(
                    act_id=int(work.id),
                    subwork_id=getWorkSubId(s.namework, '1'),
                    sum=s.sum,
                    quantity=s.quantity,
                    unitcost=s.costofpart
                )
                update_subworks_act_data = await create_mkd_works_db_object(db_session, act_subwork)
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@", update_subworks_act_data)
                if not update_subworks_act_data == 1:
                    create_subwork_act_data = await create_mkd_works_db_object(db_session, act_subwork)
                continue

            if s.workType == 'fixwork':
                act_fixwork = Acthasfixworks(
                    act_id=int(work.id),
                    fixwork_id=getWorkSubId(s.namework, '2'),
                    sum=s.sum,
                    quantity=s.quantity,
                    unitcost=s.costofpart
                )
                update_fixworks_act_data = await create_mkd_works_db_object(db_session, act_fixwork)
                if not update_fixworks_act_data == 1:
                    create_fixwork_act_data = await create_mkd_works_db_object(db_session, act_fixwork)

    print("-----------------", sum, act_edit_model_object.all_sum)
    if sum != work.all_sum:
        act_edit_model_object.all_sum = sum
        print("-----------------", sum, act_edit_model_object.all_sum)
    acts_update = await update_act_db(db_session, act_edit_model_object)
    if acts_update == 1:
        print("!!>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", acts_update)
        return             
    return {"error": "document not update"}

@router.post("/houses/works/create/")
async def create_act(
    work: WorkNewSchema,
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.MANAGEMENT_MKD_WORKS_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session)
    ):
    # если -1, то работа новая несуществующая. Доки еще добавить
    print("------------------------------------------------>>>>>>>>>>>", work.id)
    if work.id and work.id == '-1':
        print("------------------------------------------------>>>>>>>>>>>first if", work.id)
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>WORKS", work.works)
        act_create_model_object = Acts(
            id=None,
            num=work.num,
            all_sum=work.all_sum,
            month_year_works=datetime.strptime(work.month_year_works, '%Y-%m-%d') if work.month_year_works != '' else None,
            house_id=int(work.house_id),
            director=work.directorSovietFIO,
            director_appartment=work.directorAppartNum
        )
        create_db_act_data = await create_mkd_works_db_object(db_session, act_create_model_object)
        sum = 0
        if len(work.works) > 0:
            for s in work.works:
                sum = calcSum(s.sum, sum=sum)
                if s.workType == 'subwork':
                    act_subwork = Acthassubworks(
                        act_id=create_db_act_data.id,
                        subwork_id=s.workSubId if s.workSubId != -1 else getWorkSubId(s.namework, '1'),
                        sum=s.sum,
                        quantity=s.quantity,
                        unitcost=s.costofpart
                    )
                    create_subworks_act_data = await create_mkd_works_db_object(db_session, act_subwork)
                    print("#######################################", create_subworks_act_data)
                    continue

                if s.workType == 'fixwork':
                    act_fixwork = Acthasfixworks(
                        act_id=create_db_act_data.id,
                        fixwork_id=s.workSubId if s.workSubId != -1 else getWorkSubId(s.namework, '2'),
                        sum=s.sum,
                        quantity=s.quantity,
                        unitcost=s.costofpart
                    )
                    create_fixwork_act_data = await create_mkd_works_db_object(db_session, act_fixwork)

        #print("-----------------", sum, act_edit_model_object.all_sum)
        if sum != work.all_sum:
            act_create_model_object.all_sum = sum
            act_create_model_object.id = create_db_act_data.id
            #print("-----------------", sum, act_edit_model_object.all_sum)
        acts_create = await update_act_db(db_session, act_create_model_object)
        if acts_create:
            print("!!>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", acts_create)
            return             
        return {"error": "document not update", "status_code": 422}
    elif work.id and work.id != '-1':
        print("------------------------------------------------>>>>>>>>>>>second if", work.id)
        act_edit_model_object = Acts(
            id=int(work.id),
            num=work.num,
            all_sum=work.all_sum,
            month_year_works=datetime.strptime(work.month_year_works, '%Y-%m-%d') if work.month_year_works != '' else None,
            house_id=int(work.house_id),
        )
        sum = 0
        if len(work.works) > 0:
            for s in work.works:
                sum = calcSum(s.sum, sum=sum)
                if s.workType == 'subwork':
                    act_subwork = Acthassubworks(
                        act_id=int(work.id),
                        subwork_id=s.workSubId if s.workSubId != -1 else getWorkSubId(s.namework, '1'),
                        sum=s.sum,
                        quantity=s.quantity,
                        unitcost=s.costofpart
                    )
                    update_subworks_act_data = await update_acthassubworks_db(db_session, act_subwork)
                    if not update_subworks_act_data == 1:
                        create_subwork_act_data = await create_mkd_works_db_object(db_session, act_subwork)
                    continue

                if s.workType == 'fixwork':
                    act_fixwork = Acthasfixworks(
                        act_id=int(work.id),
                        subwork_id=s.workSubId if s.workSubId != -1 else getWorkSubId(s.namework, '2'),
                        sum=s.sum,
                        quantity=s.quantity,
                        unitcost=s.costofpart
                    )
                    update_fixworks_act_data = await update_acthasfixworks_db(db_session, act_fixwork)
                    if not update_fixworks_act_data == 1:
                        create_fixwork_act_data = await create_mkd_works_db_object(db_session, act_fixwork)

        #print("-----------------", sum, act_edit_model_object.all_sum)
        if sum != work.all_sum:
            act_edit_model_object.all_sum = sum
            print("-----------------", sum, act_edit_model_object.all_sum)
        acts_update = await update_act_db(db_session, act_edit_model_object)
        if acts_update == 1:
            #print("!!>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", acts_update)
            return             
        return {"error": "document not update", "status_code": 422}

@router.get("/download/act/{uuid}")
async def download_act(
    uuid: str,
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.MANAGEMENT_MKD_WORKS_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session)
    ):
    act = await select_act_doc_by_uuid(db_session, uuid)
    print("!@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",act)
    if act:
        return FileResponse(path=act.path, filename=act.name, media_type=act.filetype)


@router.get("/download/smeta/{uuid}")
async def download_act(
    uuid: str,
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.MANAGEMENT_MKD_WORKS_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session)
    ):
    smeta = await select_smeta_doc_by_uuid(db_session, uuid)
    print("!@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@", smeta)
    if smeta:
        return FileResponse(path=smeta.path, filename=smeta.name, media_type=smeta.filetype)
    

@router.get("/download/yearact/{uuid}")
async def download_year_act_file(
    uuid: str,
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.MANAGEMENT_MKD_WORKS_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session)
    ):
    year_act = await get_year_acts_file_by_year_act_uuid(db_session, uuid)
    print("!@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@", year_act.path)
    if year_act:
        return FileResponse(path=year_act.path, filename=year_act.name, media_type=year_act.filetype)    
    
@router.get("/houses/yearacts/generate/{year}/{house_id}")
async def get_all_year_acts_for_house(
    house_id: int,
    year: datetime,
    background_tasks: BackgroundTasks,
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.MANAGEMENT_MKD_WORKS_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session)
    ):
    #YearActFilesSchema, YearActfiles
    print("--------------------------------->", year, house_id)
    exist_year_act = await get_year_acts_by_house_id_and_year(db_session, year, house_id)
    if not exist_year_act:
        works_for_year_from_db = await get_acts_by_year_and_house_id(db_session, year, house_id)
        data = []
        for work in works_for_year_from_db:
            workObj = DoneWorksSchema.model_validate(work).model_dump()
            data.append(workObj)
        task_db_obj = BGTasks(
            status='start'
        )    
        task_db_record = await create_mkd_works_db_object(db_session, task_db_obj)
        
        background_tasks.add_task(genereate_year_act_xlsx_file, year, house_id, data, task_db_record.uuid, db_session)
        return {"message": "task started", "task_id": task_db_record.uuid}
    else:
        print("sssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss", exist_year_act)
        return {"message": "year act exist", "year": year.year, "act_num": exist_year_act[0].num}
    
@router.get("/houses/yearacts/task/{uuid}/status", response_model=BGTaskSchema)
async def get_bg_status_by_uuid(
    uuid: str,
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.MANAGEMENT_MKD_WORKS_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session)
    ):
    if uuid:
        task = await get_bg_task_status(db_session, uuid)
        if task:
            print(task, task.status)
            return task

    
@router.get("/houses/yearacts/all/{house_id}", response_model=list[YearActFilesSchema])
async def get_all_year_acts_for_house(
    house_id: int,
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.MANAGEMENT_MKD_WORKS_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session)
    ):
    
    selected_year_acts = await get_year_acts_by_house_id(db_session, house_id)
    return selected_year_acts

@router.post("/uploadfile/techfile")
async def create_upload_tech_file(
    houseid: Annotated[int, Form()],
    docnum: Annotated[str | None, Form()] = None,
    docdate: Annotated[datetime | None, Form()] = None,
    file: UploadFile | None = None,
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.MANAGEMENT_MKD_WORKS_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session)
    ):
    if not file:
        return {"message": "No file sent"}
    else:
        if settings.FILE_SERVER == 'localhost':
            url = '/download/techdoc/'
        else:
            url = f'https://{settings.FILE_SERVER}:{settings.FILE_SERVER_PORT}/download/techdoc/'
        timstamp1 =int(datetime.now(tz=timezone.utc).timestamp() * 1000)  
        fullpath = path.join(settings.TECH_FILES_STORE_PATH, f'{str(timstamp1)}_{file.filename}')
        techfile = Techfiles(
                name=file.filename,
                date=docdate,
                num=docnum,
                extention=get_file_extension(file.filename),
                url=url,
                path=fullpath,
                size=str(file.size),
                filetype=file.content_type,  # assuming the file type is correct in this case
                house_id=houseid,
            )
        cr_tech_doc = await create_mkd_works_db_object(db_session, techfile)
                  
        await chunked_copy(file, fullpath)
        
        return {
            "techfilename": file.filename,
            "techfiledate": docdate,
            "techfilenum": docnum,
            "url": url,
            "uuid": cr_tech_doc.uuid
            }
    
@router.get("/download/techdoc/{uuid}")
async def download_tech_file(
    uuid: str,
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.MANAGEMENT_MKD_WORKS_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session)
    ):
    techdoc = await get_techdoc_file_by_uuid(db_session, uuid)
    print("!@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@", techdoc.path)
    if techdoc:
        return FileResponse(path=techdoc.path, filename=techdoc.name, media_type=techdoc.filetype)
    
@router.get("/houses/techdocs/all/{house_id}", response_model=list[TechFilesSchema])
async def get_all_techdocs_for_house(
    house_id: int,
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.MANAGEMENT_MKD_WORKS_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session)
    ):
    
    selected_techdocs = await get_tech_files_by_house_id(db_session, house_id)
    return selected_techdocs
    
