from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker, class_mapper
from datetime import datetime
from ..settings.settings import settings
from sqlalchemy.ext.serializer import loads, dumps


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

def contacts_obj_list_to_dicts_list(row_list):
    result = []
    buf_result = None
    for row in row_list:
        #ser = dumps(row)
        print(row)
        #row_dict = row2dict(row[0])
        #print(row)
        #print(row[0].phones)
        #print(row_dict)
        """
        row_dict = row2dict(row[0])
        if not buf_result:
            row_dict['phones'] = []
            row_dict['phones'].append(row2dict(row[1]))
            row_dict['emails'] = []
            row_dict['emails'].append(row2dict(row[2]))
            row_dict['addresses'] = []
            row_dict['addresses'].append(row2dict(row[3]))
            row_dict['organisations'] = []
            row_dict['organisations'].append(row2dict(row[4]))
        elif buf_result['uuid'] == row_dict['uudi']:
            if buf_result
            row_dict['phones'].append(row2dict(row[1]))
            row_dict['emails'] = []
            row_dict['emails'].append(row2dict(row[2]))
            row_dict['addresses'] = []
            row_dict['addresses'].append(row2dict(row[3]))
            row_dict['organisations'] = []
            row_dict['organisations'].append(row2dict(row[4]))"""



    """ 
        if not buf_result:
            buf_result = row_dict
            continue
        if row_dict[orm_class_name] is buf_result[orm_class_name]:    
            for key, value in row_dict.items():
                if key != orm_class_name:
                    if not isinstance(buf_result[key], list):
                        last_value = buf_result[key]
                        buf_result[key] = [row2dict(last_value)]
                    buf_result[key].append(row2dict(value))    
        else:
            result = add_buff_to_result(buf_result, result, orm_class_name)
            buf_result = row_dict 

    for key, value in buf_result.items():
            if key != orm_class_name:
                if not isinstance(buf_result[key], list):
                    last_value = buf_result[key]
                    buf_result[key] = [last_value]
    result = add_buff_to_result(buf_result, result, orm_class_name)
    return result"""


def alchemy_json_encoder(revisit_self = False, fields_to_expand = [], fields_to_ignore = [], fields_to_replace = {}):
   """
   Serialize SQLAlchemy result into JSon
   :param revisit_self: True / False
   :param fields_to_expand: Fields which are to be expanded for including their children and all
   :param fields_to_ignore: Fields to be ignored while encoding
   :param fields_to_replace: Field keys to be replaced by values assigned in dictionary
   :return: Json serialized SQLAlchemy object
   """
   _visited_objs = []
   class AlchemyEncoder(json.JSONEncoder):
      def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # don't re-visit self
            if revisit_self:
                if obj in _visited_objs:
                    return None
                _visited_objs.append(obj)

            # go through each field in this SQLalchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata' and x not in fields_to_ignore]:
                val = obj.__getattribute__(field)
                # is this field method defination, or an SQLalchemy object
                if not hasattr(val, "__call__") and not isinstance(val, BaseQuery):
                    field_name = fields_to_replace[field] if field in fields_to_replace else field
                    # is this field another SQLalchemy object, or a list of SQLalchemy objects?
                    if isinstance(val.__class__, DeclarativeMeta) or \
                            (isinstance(val, list) and len(val) > 0 and isinstance(val[0].__class__, DeclarativeMeta)):
                        # unless we're expanding this field, stop here
                        if field not in fields_to_expand:
                            # not expanding this field: set it to None and continue
                            fields[field_name] = None
                            continue

                    fields[field_name] = val
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)
   return AlchemyEncoder
                
# Dependency
async def get_async_session() -> AsyncSession:
    async with async_session() as session:
        yield session