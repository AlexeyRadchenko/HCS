from datetime import datetime
from ..database.mkd_works.crud import create_mkd_works_db_object, get_all_subworks, get_all_fixworks, get_all_mainworks
from ..database.database import get_async_session
from ..database.mkd_works.models import Houses, Companies, Mainworks, Subworks, Fixworks
from ..database.database import async_session
from decimal import Decimal


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
    main, w_type, w_id = id_str.split('_')
    if needType == w_type:
        return int(w_id)
    return

async def test_all_works_select():
    async with async_session() as db_session:
        mainworks = await get_all_mainworks(db_session)
        subworks = await get_all_subworks(db_session)
        fixworks = await get_all_fixworks(db_session)
        print("TEST WORKS REF", len(mainworks), len(subworks), len(fixworks))