from cgitb import reset
from inspect import isclass
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker, class_mapper
from datetime import datetime
from ..settings.settings import settings


DATABASE_URL = settings.DATABASE_URL
#DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost/asyncalchemy"


engine = create_async_engine(DATABASE_URL, echo=True)

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))
    return d

def user_many2many2dict(row_list):
    d = None    
    for row in row_list:
        if not d:
            d = row2dict(row[0])
            d['scopes'] = []
        d['scopes'].append(row[1])
    return d

def add_buff_to_result(buf_result, result, orm_class_name):
    obj = row2dict(buf_result[orm_class_name])
    del buf_result[orm_class_name]
    buf_result.update(obj)
    result.append(buf_result)
    return result

def objects_many2many2dict_list(row_list, orm_class_name):
    result = []
    buf_result = None
    for row in row_list:
        row_dict = row._asdict()
        if not buf_result:
            buf_result = row_dict
            continue
        if row_dict[orm_class_name] is buf_result[orm_class_name]:    
            for key, value in row_dict.items():
                if key != orm_class_name:
                    if not isinstance(buf_result[key], list):
                        last_value = buf_result[key]
                        buf_result[key] = [last_value]
                    buf_result[key].append(value)    
        else:
            result = add_buff_to_result(buf_result, result, orm_class_name)
            buf_result = row_dict 

    for key, value in buf_result.items():
            if key != orm_class_name:
                if not isinstance(buf_result[key], list):
                    last_value = buf_result[key]
                    buf_result[key] = [last_value]
    result = add_buff_to_result(buf_result, result, orm_class_name)
    return result

                
# Dependency
async def get_async_session() -> AsyncSession:
    async with async_session() as session:
        yield session
