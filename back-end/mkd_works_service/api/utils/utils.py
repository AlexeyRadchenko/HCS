from datetime import datetime
from ..database.mkd_works.crud import (create_mkd_works_db_object, get_all_subworks, get_all_fixworks, get_all_mainworks,
    get_all_houses, update_company_work_type_subwork, update_company_work_type_fixwork, update_company_work_type_mainwork)
from ..database.database import get_async_session
from ..database.mkd_works.models import (Houses, Companies, Mainworks, Subworks, Fixworks, Acts, Acthassubworks, Acthasmainworks, Acthasfixworks)
from ..database.database import async_session
from decimal import Decimal, InvalidOperation


CHUNK_SIZE = 2 ** 20  # 1MB

async def init_mkd_works_db_data(obj_list, org):
    async with async_session() as db_session:

        if org == 1:
            companies_obj = Companies (
                id=1,
                full_name='ООО "Комфортный дом"',
                short_name='Комфортный дом',
                dirname='Е.',
                dirsurname='Мязина',
                dirsecondname='A.',
                dirname_who_what='E.',
                dirsurname_who_what='Мязиной',
                dirsecondname_who_what='А.'

            )
        if org == 2:
            companies_obj = Companies (
                id=2,
                full_name='ООО "ЖилКомСервис - Трехгорный"',
                short_name='ЖКС - Трехгорный',
                dirname='Д.',
                dirsurname='Беднарский',
                dirsecondname='Б.',
                dirname_who_what='Д.',
                dirsurname_who_what='Беднарского',
                dirsecondname_who_what='Б.'
            )
  
        company = await create_mkd_works_db_object(db_session, companies_obj)

        for data in obj_list:
            house_obj = Houses(
                street=data['street'],
                number=data['number'],
                company_id=org,
                #director=data['director'],
                #director_appartment=data['director_appartment']
            )
            house = await create_mkd_works_db_object(db_session, house_obj)
            print("insert to db ", house.street, house.number)
    print("data upload to db")


async def init_mkd_works_db_works_reference_book(mainworks_lst, subworks_lst, fixworks_lst):
    async with async_session() as db_session:
        for mainwork in mainworks_lst:
            mainwork_obj = Mainworks(
                work=f'{mainwork[0]} {mainwork[1]}',
                workType='main'
            )
            mainwork_from_db = await create_mkd_works_db_object(db_session, mainwork_obj)
            for subwork in subworks_lst:
                if mainwork[0] == subwork[0][:-2]:
                    subwork_obj = Subworks(
                        work=f'{subwork[0]} {subwork[1]}',
                        ext_works=subwork[2],
                        workType='subwork',
                        period=subwork[3],
                        base=subwork[4],
                        mainwork_id=mainwork_from_db.id,
                        numsprav=subwork[0]
                    )
                    await create_mkd_works_db_object(db_session, subwork_obj)
            for fixwork in fixworks_lst:
                if mainwork[0] == fixwork[0][:-2]:
                    fixwork_obj = Fixworks(
                        work=f'{fixwork[0]} {fixwork[1]}',
                        ext_works=fixwork[2],
                        workType='fixwork',
                        period=fixwork[3],
                        base=fixwork[4],
                        mainwork_id=mainwork_from_db.id,
                        numsprav=fixwork[0]
                    )
                    await create_mkd_works_db_object(db_session, fixwork_obj)
    print("data upload to db")

def find_upload_house_id (upload_house, houses_from_db):
    split_upload_house = upload_house.strip().split(' ')
    street = ' '.join(split_upload_house[:-1])
    number = split_upload_house[-1].upper()
    for db_house in houses_from_db:
        if not db_house.street == street:
            continue
        elif not db_house.number == number:
            continue
        else:
            return db_house.id
    return

def find_upload_work_in_db (upload_work_name, works_in_db):
    for db_work in works_in_db:
        if db_work.work == upload_work_name.rstrip():
            return db_work
    return

def validate_work_in_db(work, mainworks_in_db, subworks_in_db, fixworks_in_db):
    model_work_type = None
    mainwork = find_upload_work_in_db(work['Нименование работы(услуги)'], mainworks_in_db)
    if not mainwork:
        subwork = find_upload_work_in_db(work['Нименование работы(услуги)'], subworks_in_db)
        if not subwork:
            fixwork = find_upload_work_in_db(work['Нименование работы(услуги)'], fixworks_in_db)
            if not fixwork:
                raise ValueError(f"В базе не найдено название работы {work['Нименование работы(услуги)']}", work)
            else:
                model_work_type = 'fix'
        else:
            model_work_type = 'sub'         
    else:
        model_work_type = 'main'
    work_id = mainwork.id if model_work_type == 'main' else subwork.id if model_work_type == 'sub' else fixwork.id
    return model_work_type, work_id            


async def upload_mkd_works_from_xlsx_to_db_util(mainworks_lst, org):
    model_works_map = {
        'main': {
            'model': Acthasmainworks,
            'id_attr': lambda work_obj, id : setattr(work_obj, 'mainwork_id', id)
        },
        'sub': {
            'model': Acthassubworks,
            'id_attr': lambda work_obj, id : setattr(work_obj, 'subwork_id', id)
            }, 
        'fix': {
            'model': Acthasfixworks,
            'id_attr': lambda work_obj, id : setattr(work_obj, 'fixwork_id', id)
        }
    }
     
    async with async_session() as db_session:
        houses = await get_all_houses(db_session)
        mainworks_in_db = await get_all_mainworks(db_session)
        subworks_in_db = await get_all_subworks(db_session)
        fixworks_in_db = await get_all_fixworks(db_session)
        for work in mainworks_lst:
            house_id = find_upload_house_id(work['Адрес дома'], houses)
            model_work_type = None
            if not house_id:
                raise ValueError(f"В базе не найден адрес {work['Адрес дома']}")
            else:
                act = Acts(
                    date=work['Месяц и год проведения работ'],
                    num=work['Номер сметы'],
                    all_sum=str(work['Цена выполненной работы (оказанной услуги) в рублях']),
                    month_year_works=work['Месяц и год проведения работ'],
                    work_square=str(work['Кол-во единиц измерений']),
                    unit_cost=str(work['Стоимость оказанной услуги за единицу, руб/м2']),
                    house_id=house_id,
                )
                created_act = await create_mkd_works_db_object(db_session, act)
                        
            model_work_type, work_id = validate_work_in_db(work, mainworks_in_db, subworks_in_db, fixworks_in_db)
            if model_work_type:
                model_work = model_works_map[model_work_type]['model']
                work_obj = model_work(
                    act_id=created_act.id,
                    sum=str(work['Цена выполненной работы (оказанной услуги) в рублях']),
                    quantity=str(work['Кол-во единиц измерений']),
                    unitcost=str(work['Стоимость оказанной услуги за единицу, руб/м2']),
                    notes=work['коментарий'],
                    act_custom_period=work['Периодичность'],
                )
                
                model_works_map[model_work_type]['id_attr'](work_obj, work_id)
                await create_mkd_works_db_object(db_session, work_obj)
        print("data upload to db")
        await db_session.commit()
        await db_session.close()
        

async def chunked_copy(src, dst):
    await src.seek(0)
    with open(dst, "wb") as buffer:
        while True:
            contents = await src.read(CHUNK_SIZE)
            if not contents:
                print(f"Src completely consumed\n")
                break
            print(f"Consumed {len(contents)} bytes from Src file\n")
            buffer.write(contents)

def get_file_extension(filname):
    return filname.split('.')[-1]

def calcSum(*args, **kwargs):
    s = Decimal(kwargs.get('sum', 0))
    for arg in args:
        s += Decimal(arg)
    return str(s)

def getWorkSubId(id_str, needType):
    if needType == '0':
        return int(id_str)
    
    main, w_type, w_id = id_str.split('_')

    #print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@', id_str, needType, main, w_type, w_id)
    if needType == w_type:
        return int(w_id)
    
    return

async def test_all_works_select():
    async with async_session() as db_session:
        mainworks = await get_all_mainworks(db_session)
        subworks = await get_all_subworks(db_session)
        fixworks = await get_all_fixworks(db_session)
       #print("TEST WORKS REF", len(mainworks), len(subworks), len(fixworks))

def sorting_works_group(works):
    sorted_data = sorted(works, key=lambda x: x['main_work_id'])
    for gwork in works:
        gwork['works'] = sorted(gwork['works'], key=lambda w: w['work_id'])

    return sorted_data  

async def update_company_work_type (data, work_type):
    update_call_map = {
        'mainwork': update_company_work_type_mainwork,
        'subwork': update_company_work_type_subwork,
        'fixwork': update_company_work_type_fixwork,
    }
    async with async_session() as db_session:
        for work in data:
            res = await update_call_map[work_type](db_session, work)
            if res:
                print("update company work type", work)
            else:
                print("update company work type error", work)
                await db_session.close()
                break
        await db_session.close()
        print("data upload to db")
 