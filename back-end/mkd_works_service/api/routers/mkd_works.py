from fastapi import APIRouter, Depends, Security, UploadFile, Form, BackgroundTasks
from fastapi.responses import JSONResponse, FileResponse
from sqlalchemy.ext.asyncio.session import AsyncSession
from typing import List, Annotated
from datetime import datetime, timezone
from os import path

from ..database.mkd_works.schemas import (HousesMKDSchema, DoneWorksSchema, ReferenceBookSchema, WorkEditSchema, WorkNewSchema, YearActFilesSchema, 
    BGTaskSchema, TechFilesSchema, MonthActFilesSchema)
from ..database.mkd_works.crud import (
    get_all_houses, get_all_mkd_works_by_house_id, get_furure_work_id_from_db, create_mkd_works_db_object, get_all_mainworks,
    get_all_subworks, get_all_fixworks, update_act_db, update_acthasfixworks_db, update_acthassubworks_db, select_act_doc_by_uuid,
    select_smeta_doc_by_uuid, get_year_acts_by_house_id, get_acts_by_year_and_house_id, get_year_acts_by_house_id_and_year, get_bg_task_status,
    get_year_acts_file_by_year_act_uuid, get_techdoc_file_by_uuid, get_tech_files_by_house_id, delete_act_old_works,
    get_mkd_director_data_from_db_by_house_id, get_month_acts_by_house_id, get_month_acts_files_data_by_house_id_and_month_year, 
    get_acts_by_month_year_and_house_id, get_month_acts_file_by_year_act_uuid, create_mkd_works_db_objects, update_act_has_actfiles_db,
    update_act_has_smetafiles_db, select_act_doc_by_uuid_and_act_id, select_smeta_doc_by_uuid_and_act_id, get_month_acts_full_list
    )
from ..database.mkd_works.models import (Acts, Actfiles, Actshasactfiles, Smetafiles, Actshassmetafiles, Acthasmainworks, Acthassubworks, Acthasfixworks, BGTasks,
    Techfiles)
from api.security.acess_depends import user_scope_authorize
from ..database.database import get_async_session
from api.settings.settings import settings
from ..utils.utils import chunked_copy, get_file_extension, calcSum, getWorkSubId
from ..tasks.tasks import genereate_year_act_xlsx_file
from ..tasks.task_v2 import genereate_year_act_xlsx_file_v2, genereate_month_act_xlsx_file_v2



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
    #print(">>>>>>>>>>>>>>>>>>>>>>FIXWORKS", len(all_works_by_house_id[0].fixworks), all_works_by_house_id[0].fixworks[0].work)
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
        
        if not workid or workid in ('', 'undefined'):
            acthasactfiles = None
            #print("not exist", workid)
            """act = Acts(
                house_id=houseid,
                all_sum='0',
            )
            cr_work = await create_mkd_works_db_object(db_session, act)
            acthasactfiles = Actshasactfiles(
                act_id=0,
                actfile_uuid=cr_act_doc.uuid
            )"""
            workid="-1"
        else:
            #print("exist", workid)
            #create act document with ref to act.id=workid
            acthasactfiles = Actshasactfiles(
                act_id=int(workid),
                actfile_uuid=cr_act_doc.uuid
            )    
        await chunked_copy(file, fullpath)
        if acthasactfiles:
            ref_obj = await create_mkd_works_db_object(db_session, acthasactfiles)
        return {
            "filename": file.filename,
            "actdate": actdate,
            "actnum": actnum,
            "url": url,
            "uuid": cr_act_doc.uuid,
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

        if not workid or workid in ('', 'undefined'):
            acthassmetafiles = None
            #print("not exist", workid)
            """act = Acts(
                house_id=houseid,
                all_sum='0',
            )
            cr_work = await create_mkd_works_db_object(db_session, act)
            acthassmetafiles = Actshassmetafiles(
                act_id=cr_work.id,
                smetafile_uuid=cr_smeta_doc.uuid
            )"""
            workid="-1"
        else:
            #print("exist", workid)
            #create act document with ref to act.id=workid
            acthassmetafiles = Actshassmetafiles(
                act_id=int(workid),
                smetafile_uuid=cr_smeta_doc.uuid
            )            
        await chunked_copy(file, fullpathsmeta)
        if acthassmetafiles:
            ref_obj = await create_mkd_works_db_object(db_session, acthassmetafiles)
        return {
            "filename": file.filename,
            "smetadate": smetadate,
            "smetanum": smetanum,
            "url": url,
            "uuid": cr_smeta_doc.uuid,
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
    #print("++++++++++++++++++++++++++++++++++", mainworks)
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
    #print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>WORKS", work.works)
    #print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>WORK ID", int(work.id))
    #print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>WORK", work)
    res = None
    if len(work.mainworks) > 0:
        res = await delete_act_old_works(db_session, int(work.id), 'mainworks')
        #print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>WORKS_DEL_MAINWORKS", res)
    if len(work.subworks) > 0:
        res = await delete_act_old_works(db_session, int(work.id), 'subworks')
        #print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>WORKS_DEL_SUBWORKS", res)
    if len(work.fixworks) > 0:
        res = await delete_act_old_works(db_session, int(work.id), 'fixworks')
        #print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>WORKS_DEL_FIXWORKS", res)
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
        objects_to_add = []
        for s in work.works:
            sum = calcSum(s.sum, sum=sum)
            #print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>WORKS", s.period)
            if s.workType == 'mainwork':
                act_mainwork = Acthasmainworks(
                    act_id=int(work.id),
                    mainwork_id=s.workSubId if s.workSubId != -1 else getWorkSubId(s.namework, '0'),
                    sum=s.sum,
                    quantity=s.quantity,
                    unitcost=s.costofpart,
                    notes = s.notes,
                    act_custom_period = s.period
                )
                #create_mainwork_act_data = await create_mkd_works_db_object(db_session, act_mainwork)
                #print("####################################### CREATE NEW MAINWORK", act_mainwork.mainwork_id, act_mainwork.act_id, act_mainwork.act_custom_period)
                objects_to_add.append(act_mainwork)
                continue
            if s.workType == 'subwork':
                act_subwork = Acthassubworks(
                    act_id=int(work.id),
                    subwork_id=getWorkSubId(s.namework, '1'),
                    sum=s.sum,
                    quantity=s.quantity,
                    unitcost=s.costofpart,
                    act_custom_period = s.period
                )
                #update_subworks_act_data = await create_mkd_works_db_object(db_session, act_subwork)
                #print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@", update_subworks_act_data)
                objects_to_add.append(act_subwork)
                #if not update_subworks_act_data == 1:
                #    create_subwork_act_data = await create_mkd_works_db_object(db_session, act_subwork)
                continue

            if s.workType == 'fixwork':
                act_fixwork = Acthasfixworks(
                    act_id=int(work.id),
                    fixwork_id=getWorkSubId(s.namework, '2'),
                    sum=s.sum,
                    quantity=s.quantity,
                    unitcost=s.costofpart,
                    act_custom_period = s.period
                )
                #update_fixworks_act_data = await create_mkd_works_db_object(db_session, act_fixwork)
                #print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@UPDATE", update_fixworks_act_data.act_custom_period)
                #if not update_fixworks_act_data == 1:
                #    create_fixwork_act_data = await create_mkd_works_db_object(db_session, act_fixwork)
                objects_to_add.append(act_fixwork)
        res = await create_mkd_works_db_objects(db_session, objects_to_add)
        #print("#######################################", res)

    #print("-----------------", sum, act_edit_model_object.all_sum)
    if sum != work.all_sum:
        act_edit_model_object.all_sum = sum
        #print("-----------------", sum, act_edit_model_object.all_sum)
    acts_update = await update_act_db(db_session, act_edit_model_object)
    if acts_update == 1:
        #print("!!!!!!!!!!!!!!ACTID:", work.actUUID)
        #print("!!!!!!!!!!!!!!SMETAID:", work.smetaUUID)
        if work.actUUID:
            exist_act_files = await select_act_doc_by_uuid_and_act_id(db_session, work.actUUID, int(work.id))
            if not exist_act_files:
                act_file_update = await update_act_has_actfiles_db(db_session, int(work.id), work.actUUID)
        if work.smetaUUID:
            exist_smeta_files = await select_smeta_doc_by_uuid_and_act_id(db_session, work.smetaUUID, int(work.id))
            if not exist_smeta_files:
                smeta_file_update = await update_act_has_smetafiles_db(db_session, int(work.id), work.smetaUUID)
    if acts_update == 1:
        #print("!!>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", acts_update)
        return             
    return {"error": "document not update"}

@router.post("/houses/works/create/")
async def create_act(
    work: WorkNewSchema,
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.MANAGEMENT_MKD_WORKS_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session)
    ):
    # если -1, то работа новая несуществующая. Доки еще добавить
    #print("------------------------------------------------>>>>>>>>>>>", work)
    #print("------------------------------------------------>>>>>>>>>>>", work.id)
    if work.id and work.id == '-1':
        #print("------------------------------------------------>>>>>>>>>>>first if", work.id)
        #print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>WORKS", work.works)
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
                if s.workType == 'mainwork':
                    act_mainwork = Acthasmainworks(
                        act_id=create_db_act_data.id,
                        mainwork_id=getWorkSubId(s.workSubId, '0') if s.workSubId != -1 else getWorkSubId(s.namework, '0'),
                        sum=s.sum,
                        quantity=s.quantity,
                        unitcost=s.costofpart,
                        notes = s.notes,
                        act_custom_period = s.period
                        
                    )
                    create_mainwork_act_data = await create_mkd_works_db_object(db_session, act_mainwork)
                    #print("#######################################", create_mainwork_act_data)
                    continue
                if s.workType == 'subwork':
                    act_subwork = Acthassubworks(
                        act_id=create_db_act_data.id,
                        subwork_id=getWorkSubId(s.workSubId, '1') if s.workSubId != -1 else getWorkSubId(s.namework, '1'),
                        sum=s.sum,
                        quantity=s.quantity,
                        unitcost=s.costofpart,
                        notes = s.notes,
                        act_custom_period = s.period
                    )
                    create_subworks_act_data = await create_mkd_works_db_object(db_session, act_subwork)
                    #print("#######################################", create_subworks_act_data)
                    continue

                if s.workType == 'fixwork':
                    #print("3333333333333333333", s.workSubId, s.namework)
                    #print("$4444444444", getWorkSubId(s.namework, '2'))
                    act_fixwork = Acthasfixworks(
                        act_id=create_db_act_data.id,
                        fixwork_id=getWorkSubId(s.workSubId, '2') if s.workSubId != -1 else getWorkSubId(s.namework, '2'),
                        sum=s.sum,
                        quantity=s.quantity,
                        unitcost=s.costofpart,
                        notes = s.notes,
                        act_custom_period = s.period
                    )
                    create_fixwork_act_data = await create_mkd_works_db_object(db_session, act_fixwork)

        #print("-----------------", sum, act_edit_model_object.all_sum)
        if sum != work.all_sum:
            act_create_model_object.all_sum = sum
            act_create_model_object.id = create_db_act_data.id
            #print("-----------------", sum, act_edit_model_object.all_sum)
        acts_create = await update_act_db(db_session, act_create_model_object)
        if acts_create:
            #print("!!>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", acts_create)
            #print("!!!!!!!!!!!!!!ACTID:", work.actUUID)
            #print("!!!!!!!!!!!!!!SMETAID:", work.smetaUUID)
            if work.smetaUUID:
                exist_act_files = await select_act_doc_by_uuid_and_act_id(db_session, work.actUUID, int(work.id))
                if not exist_act_files:
                    acthassmetafiles = Actshassmetafiles(
                        act_id=create_db_act_data.id,
                        smetafile_uuid=work.smetaUUID
                    )
                    act_file_attach = await create_mkd_works_db_object(db_session, acthassmetafiles)
                else:
                    return {"error": f"document not update act exist with uuid: {work.actUUID}", "status_code": 422}
            if work.actUUID:
                exist_smeta_files = await select_smeta_doc_by_uuid_and_act_id(db_session, work.smetaUUID, int(work.id))
                if not exist_smeta_files:
                    actshasactfiles = Actshasactfiles(
                        act_id=create_db_act_data.id,
                        actfile_uuid=work.actUUID
                    )
                    act_file_attach = await create_mkd_works_db_object(db_session, actshasactfiles)
                else:
                    return {"error": f"document not update smeta exist with uuid: {work.smetaUUID}", "status_code": 422}
            return             
        return {"error": "document not update", "status_code": 422}
    

@router.get("/download/act/{uuid}")
async def download_act(
    uuid: str,
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.MANAGEMENT_MKD_WORKS_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session)
    ):
    act = await select_act_doc_by_uuid(db_session, uuid)
    #print("!@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",act)
    if act:
        return FileResponse(path=act.path, filename=act.name, media_type=act.filetype)


@router.get("/download/smeta/{uuid}")
async def download_act(
    uuid: str,
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.MANAGEMENT_MKD_WORKS_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session)
    ):
    smeta = await select_smeta_doc_by_uuid(db_session, uuid)
    #print("!@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@", smeta)
    if smeta:
        return FileResponse(path=smeta.path, filename=smeta.name, media_type=smeta.filetype)
    

@router.get("/download/yearact/{uuid}")
async def download_year_act_file(
    uuid: str,
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.MANAGEMENT_MKD_WORKS_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session)
    ):
    year_act = await get_year_acts_file_by_year_act_uuid(db_session, uuid)
    #print("!@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@", year_act.path)
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
        #print("WORKS ON YEAR __________", len(works_for_year_from_db))
        data = []
        for work in works_for_year_from_db:
            workObj = DoneWorksSchema.model_validate(work).model_dump()
            data.append(workObj)
        task_db_obj = BGTasks(
            status='start'
        )
        if len(data) == 0:
            return {"message": "Works not found", "month": year.year}
        #print("WORKS ON YEAR __________", len(data))   
        task_db_record = await create_mkd_works_db_object(db_session, task_db_obj)

        #background_tasks.add_task(genereate_year_act_xlsx_file, year, house_id, data, task_db_record.uuid, db_session)
        background_tasks.add_task(genereate_year_act_xlsx_file_v2, year, house_id, data, task_db_record.uuid, db_session)
        return {"message": "task started", "task_id": task_db_record.uuid}
    else:
        #print("sssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss", exist_year_act)
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
            #print(task, task.status)
            return task

    
@router.get("/houses/yearacts/all/{house_id}", response_model=list[YearActFilesSchema])
async def get_all_year_acts_for_house(
    house_id: int,
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.MANAGEMENT_MKD_WORKS_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session)
    ):
    
    selected_year_acts = await get_year_acts_by_house_id(db_session, house_id)
    return selected_year_acts

@router.get("/houses/monthacts/generate/{month_year}/{house_id}")
async def generate_all_month_acts_for_house(
    house_id: int,
    month_year: datetime,
    background_tasks: BackgroundTasks,
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.MANAGEMENT_MKD_WORKS_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session)
    ):
    #YearActFilesSchema, YearActfiles
    #print("--------------------------------->", year, house_id)
    if house_id == -1:
        house_id = None
    exist_month_act = await get_month_acts_files_data_by_house_id_and_month_year(db_session, month_year, house_id)
    if not exist_month_act:
        works_for_month_from_db = await get_acts_by_month_year_and_house_id(db_session, month_year, house_id)
        #print("WORKS ON MONTH __________", len(works_for_month_from_db))
        data = []
        for work in works_for_month_from_db:
            workObj = DoneWorksSchema.model_validate(work).model_dump()
            data.append(workObj)
        task_db_obj = BGTasks(
            status='start'
        )
        if len(data) == 0:
            return {"message": "Works not found", "month": month_year.month}
        #print("WORKS ON MONTH __________", len(data))   
        task_db_record = await create_mkd_works_db_object(db_session, task_db_obj)

        #background_tasks.add_task(genereate_year_act_xlsx_file, year, house_id, data, task_db_record.uuid, db_session)
        background_tasks.add_task(genereate_month_act_xlsx_file_v2, month_year, data, task_db_record.uuid, db_session, house_id)
        return {"message": "task started", "task_id": task_db_record.uuid}
    else:
        #print("sssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss", exist_month_act)
        return {"message": "month act exist", "month": month_year.month, "act_num": exist_month_act[0].num}
    
@router.get("/houses/monthacts/generate/{month_year}")
async def generate_all_month_acts_for_all_houses(
    month_year: datetime,
    background_tasks: BackgroundTasks,
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.MANAGEMENT_MKD_WORKS_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session)
    ):
    exist_month_act = await get_month_acts_files_data_by_house_id_and_month_year(db_session, month_year, house_id=None)
    if not exist_month_act:
        works_for_month_from_db = await get_acts_by_month_year_and_house_id(db_session, month_year, house_id=None)
        #print("WORKS ON MONTH __________", len(works_for_month_from_db))
        data = []
        for work in works_for_month_from_db:
            workObj = DoneWorksSchema.model_validate(work).model_dump()
            data.append(workObj)
        task_db_obj = BGTasks(
            status='start'
        )
        if len(data) == 0:
            return {"message": "Works not found", "month": month_year.month}
        #print("WORKS ON MONTH __________", len(data))   
        task_db_record = await create_mkd_works_db_object(db_session, task_db_obj)

        #background_tasks.add_task(genereate_year_act_xlsx_file, year, house_id, data, task_db_record.uuid, db_session)
        background_tasks.add_task(genereate_month_act_xlsx_file_v2, month_year, data, task_db_record.uuid, db_session)
        return {"message": "task started", "task_id": task_db_record.uuid}
    else:
        #print("sssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss", exist_month_act)
        return {"message": "month act exist", "month": month_year.month, "act_num": exist_month_act[0].num}    
    
@router.get("/houses/monthacts/task/{uuid}/status", response_model=BGTaskSchema)
async def get_bg_status_by_uuid(
    uuid: str,
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.MANAGEMENT_MKD_WORKS_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session)
    ):
    if uuid:
        task = await get_bg_task_status(db_session, uuid)
        if task:
            #print(task, task.status)
            return task
        
@router.get("/download/monthact/{uuid}")
async def download_month_act_file(
    uuid: str,
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.MANAGEMENT_MKD_WORKS_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session)
    ):
    month_act = await get_month_acts_file_by_year_act_uuid(db_session, uuid)
    #print("!@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@", year_act.path)
    if month_act:
        return FileResponse(path=month_act.path, filename=month_act.name, media_type=month_act.filetype)        

@router.get("/houses/monthacts/all/{house_id}", response_model=list[MonthActFilesSchema])
async def get_all_month_acts_for_house(
    house_id: int,
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.MANAGEMENT_MKD_WORKS_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session)
    ):
    
    selected_month_acts = await get_month_acts_by_house_id(db_session, house_id)
    return selected_month_acts

@router.get("/houses/monthacts/all", response_model=list[MonthActFilesSchema])
async def get_all_month_acts(
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.MANAGEMENT_MKD_WORKS_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session)
    ):
    
    selected_month_acts = await get_month_acts_full_list(db_session)

    return selected_month_acts

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
    #print("!@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@", techdoc.path)
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
    
@router.get("/house/{house_id}/director", response_model=HousesMKDSchema)
async def get_mkd_director_data_by_house_id(
    house_id: int,
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.MANAGEMENT_MKD_WORKS_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session)
    ):
    director_data = await get_mkd_director_data_from_db_by_house_id(db_session, house_id)
    #(">>>>>>>>>>>>>>>>>>>>>>", director_data, house_id)
    #print(">>>>>>>>>>>>>>>>>>>>>>", all_works_by_house_id[0].subworks)
    return director_data
