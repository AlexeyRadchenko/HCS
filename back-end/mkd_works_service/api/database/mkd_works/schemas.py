from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Any
from pydantic import BaseModel
from uuid import UUID


class CompaniesMKDScheme(BaseModel):
    id: int
    full_name: Optional[str]
    short_name: Optional[str]
    dirname: Optional[str]
    dirsurname: Optional[str]
    dirsecondname: Optional[str]
    dirname_who_what: Optional[str]
    dirsurname_who_what: Optional[str]
    dirsecondname_who_what: Optional[str]
    

    class Config:
        from_attributes = True

class HousesMKDSchema(BaseModel):
    id: Optional[int]
    street: Optional[str]
    number: Optional[str]
    company_id: Optional[int]
    companies: Optional[CompaniesMKDScheme]
    house_square: Optional[float]
    director_fio: Optional[str]
    director_appartment: Optional[str]

    class Config:
        from_attributes = True
        

"""class MainWorksSchema(BaseModel):
    id: Optional[int]
    work: Optional[str]
    workType: Optional[str]
    companyWorkType: Optional[str]
    notes: Optional[str]
    period: Optional[str] = None
    act_custom_period: Optional[str]=None

    class Config:
        from_attributes = True"""

class MainWorksSchema(BaseModel):
    id: Optional[int]
    work: Optional[str]
    workType: Optional[str]
    companyWorkType: Optional[str]
    numsprav: Optional[str]
    period: Optional[str] = None
    sum: Optional[str]
    quantity: Optional[str]
    unitcost: Optional[str]
    notes: Optional[str]
    mainwork_id: Optional[int] = None
    act_custom_period: Optional[str]=None

    class Config:
        from_attributes = True

class ActHasSubworksScheme(BaseModel):
    act_id: Optional[int]
    subwork_id: Optional[int]
    sum: Optional[str]
    quantity: Optional[str]
    unitcost: Optional[str]
    notes: Optional[str]
    act_custom_period: Optional[str]=None
    work: Optional[str]=None
    workType: Optional[str]=None
    companyWorkType: Optional[str]=None
    period: Optional[str]=None
    numsprav: Optional[str]=None

    class Config:
        from_attributes = True

class ActHasMainworksScheme(BaseModel):
    act_id: Optional[int]
    mainwork_id: Optional[int]
    sum: Optional[str]
    quantity: Optional[str]
    unitcost: Optional[str]
    notes: Optional[str]
    act_custom_period: Optional[str]=None
    work: Optional[str]=None
    workType: Optional[str]=None
    companyWorkType: Optional[str]=None
    period: Optional[str]=None
    numsprav: Optional[str]=None

    class Config:
        from_attributes = True

class ActHasFixworksScheme(BaseModel):
    act_id: Optional[int]
    fixwork_id: Optional[int]
    sum: Optional[str]
    quantity: Optional[str]
    unitcost: Optional[str]
    notes: Optional[str]
    act_custom_period: Optional[str]=None
    work: Optional[str]=None
    workType: Optional[str]=None
    companyWorkType: Optional[str]=None
    period: Optional[str]=None
    numsprav: Optional[str]=None

    class Config:
        from_attributes = True                   

class SubWorksSchema(BaseModel):
    id: Optional[int]
    work: Optional[str]
    ext_works: Optional[str]
    workType: Optional[str]
    companyWorkType: Optional[str]
    period: Optional[str]
    base: Optional[str]
    numsprav: Optional[str]
    mainwork_id: Optional[int]
    sum: Optional[str]
    quantity: Optional[str]
    unitcost: Optional[str]
    notes: Optional[str]
    act_custom_period: Optional[str]=None

    class Config:
        from_attributes = True

class FixWorksSchema(BaseModel):
    id: Optional[int]
    work: Optional[str]
    ext_works: Optional[str]
    workType: Optional[str]
    companyWorkType: Optional[str]
    period: Optional[str]
    base: Optional[str]
    numsprav: Optional[str]
    mainwork_id: Optional[int]
    sum: Optional[str]
    quantity: Optional[str]
    unitcost: Optional[str]
    notes: Optional[str]
    act_custom_period: Optional[str]=None

    class Config:
        from_attributes = True

class ActFilesSchema(BaseModel):
    uuid: Optional[UUID]
    name: Optional[str]
    date: Optional[datetime]
    num: Optional[str]
    extention: Optional[str]
    url: Optional[str]
    path: Optional[str]
    size: Optional[str]
    filetype: Optional[str]
    house_id: Optional[int]
    date_upload: Optional[datetime]

    class Config:
        from_attributes = True

class SmetaFilesSchema(BaseModel):
    uuid: Optional[UUID]
    name: Optional[str]
    date: Optional[datetime]
    num: Optional[str]
    extention: Optional[str]
    url: Optional[str]
    path: Optional[str]
    size: Optional[str]
    filetype: Optional[str]
    house_id: Optional[int]
    date_upload: Optional[datetime]

    class Config:
        from_attributes = True

class TechFilesSchema(BaseModel):
    uuid: Optional[UUID]
    name: Optional[str]
    date: Optional[datetime]
    num: Optional[str]
    extention: Optional[str]
    url: Optional[str]
    path: Optional[str]
    size: Optional[str]
    filetype: Optional[str]
    house_id: Optional[int]
    date_upload: Optional[datetime]

    class Config:
        from_attributes = True    

class DoneWorksSchema(BaseModel):
    id: Optional[int]
    date: Optional[datetime]
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    num: Optional[str]
    house_id: Optional[int]
    all_sum: Optional[str]
    unit_cost: Optional[str]
    work_square: Optional[str]
    month_year_works: Optional[datetime]
    director: Optional[str]
    director_appartment: Optional[str]
    houses:Optional[HousesMKDSchema]
    mainworks: List[MainWorksSchema]
    subworks: List[FixWorksSchema]
    fixworks: List[SubWorksSchema]
    mainworks_details: List[ActHasMainworksScheme]
    subworks_details: List[ActHasSubworksScheme]
    fixworks_details: List[ActHasFixworksScheme]
    actfiles: List[ActFilesSchema]
    smetafiles: List[SmetaFilesSchema]

    class Config:
        from_attributes = True

class ReferenceMainWorkSchema(BaseModel):
    id: Optional[int]
    work: Optional[str]

    class Config:
        from_attributes = True

class ReferenceSubworkSchema(BaseModel):
    id: Optional[int]
    work: Optional[str]
    ext_works: Optional[str]
    workType: Optional[str]
    period: Optional[str]
    base: Optional[str]
    mainwork_id: Optional[int]

    class Config:
        from_attributes = True

class ReferenceFixworkSchema(BaseModel):
    id: Optional[int]
    work: Optional[str]
    ext_works: Optional[str]
    workType: Optional[str]
    period: Optional[str]
    base: Optional[str]
    mainwork_id: Optional[int]

    class Config:
        from_attributes = True        

class ReferenceBookSchema(BaseModel):
    mainworks: List[ReferenceMainWorkSchema]
    fixworks: List[ReferenceSubworkSchema]
    subworks: List[ReferenceFixworkSchema]

    class Config:
        from_attributes = True



class TableWorkRowEditSchema(BaseModel):
    numsprav: Optional[str]
    namework: Optional[str]
    period: Optional[str]
    quantity: Optional[str]
    costofpart: Optional[str]
    sum: Optional[str]
    workType: Optional[str]
    workSubId: Optional[int]
    notes: Optional[str] = None

class TableWorkNewSchema(BaseModel):
    numsprav: Optional[str] = None
    namework: Optional[str] 
    period: Optional[str] = None
    quantity: Optional[str] = None
    costofpart: Optional[str] = None
    sum: Optional[str] = None
    workType: Optional[str] = None
    workSubId: Optional[int] = None
    notes: Optional[str] = None  

class EditWorksListSchema(BaseModel):
    id: Optional[int]
    workType: Optional[str]

class WorkEditSchema(BaseModel):
    id: Optional[str] 
    num: Optional[str]
    house_id: Optional[int]
    all_sum: Optional[str]
    directorSovietFIO: Optional[str]
    directorAppartNum: Optional[str]  
    month_year_works: Optional[datetime]
    works: List[TableWorkRowEditSchema]
    mainworks:List[EditWorksListSchema]
    subworks:List[EditWorksListSchema]
    fixworks:List[EditWorksListSchema]

class WorkNewSchema(BaseModel):
    id: Optional[str]
    num: Optional[str] = None
    house_id: Optional[int]
    all_sum: Optional[str] = None
    directorSovietFIO: Optional[str] = None
    directorAppartNum: Optional[str] = None
    month_year_works: datetime | str = None
    works: List[TableWorkNewSchema]
    mainworks:List[EditWorksListSchema] | None = None
    subworks:List[EditWorksListSchema] | None = None 
    fixworks:List[EditWorksListSchema] | None = None   

class YearActFilesSchema(BaseModel):
    uuid: Optional[UUID]
    name: Optional[str]
    date: Optional[datetime]
    year: Optional[datetime] = None
    num: Optional[str]
    extention: Optional[str]
    url: Optional[str]
    path: Optional[str]
    size: Optional[str]
    filetype: Optional[str]
    house_id: Optional[int]
    date_upload: Optional[datetime]

    class Config:
        from_attributes = True

class MonthActFilesSchema(BaseModel):
    uuid: Optional[UUID]
    name: Optional[str]
    date: Optional[datetime]
    month_year: Optional[datetime] = None
    num: Optional[str]
    extention: Optional[str]
    url: Optional[str]
    path: Optional[str]
    size: Optional[str]
    filetype: Optional[str]
    house_id: Optional[int]
    date_upload: Optional[datetime]

    class Config:
        from_attributes = True        

class BGTaskSchema(BaseModel):
    uuid: UUID
    status: str
    start_datetime: datetime
    end_datetime: Optional[datetime] | None
    type: Optional[str]
    percent: Optional[str]

    class Config:
        from_attributes = True     