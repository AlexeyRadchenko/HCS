from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from ..settings.settings import settings



DATABASE_URL = settings.DATABASE_URL

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

                
# Dependency
async def get_async_session() -> AsyncSession:
    async with async_session() as session:
        yield session