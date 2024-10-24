from datetime import datetime
from ..database.mkd_works.crud import create_mkd_works_db_object
from ..database.database import get_async_session
from ..database.mkd_works.models import Houses, Companies
from ..database.database import async_session


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
                dirsecondname='A.'

            )
        if org == 2:
            companies_obj = Companies (
                id=2,
                full_name='ООО "ЖилКомСервис - Трехгорный"',
                short_name='ЖКС - Трехгорный',
                dirname='Д.',
                dirsurname='Беднарский',
                dirsecondname='Б.'
            )
  
        company = await create_mkd_works_db_object(db_session, companies_obj)

        for data in obj_list:
            house_obj = Houses(
                street=data['street'],
                number=data['number'],
                company_id=org,
                director=data['director'],
                director_appartment=data['director_appartment']
            )
            house = await create_mkd_works_db_object(db_session, house_obj)
            print("insert to db ", house.street, house.number)
    print("data upload to db")


async def init_mkd_works_db_works_reference_book(mainworks_lst, subworks_lst, fixworks_lst):
    async with async_session() as db_session:
        pass
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