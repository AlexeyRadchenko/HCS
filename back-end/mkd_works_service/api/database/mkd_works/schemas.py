from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Any
from pydantic import BaseModel
from uuid import UUID

class HousesMKDSchema(BaseModel):
    id: Optional[int]
    street: Optional[str]
    number: Optional[str]
    company_id: Optional[str]
    director: Optional[str]
    director_appartment: Optional[str]
    company_id: Optional[int]

    class Config:
        from_attributes = True
        

class MainWorksSchema(BaseModel):
    id: Optional[int]
    work: Optional[str]
    workType: Optional[str]
    companyWorkType: Optional[str]

    class Config:
        from_attributes = True

class ActHasSubworksScheme(BaseModel):
    act_id: Optional[int]
    subwork_id: Optional[int]
    sum: Optional[str]
    quantity: Optional[str]
    unitcost: Optional[str]

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
    houses:Optional[HousesMKDSchema]
    mainworks: List[MainWorksSchema]
    subworks: List[SubWorksSchema]
    fixworks: List[FixWorksSchema]
    actfiles: List[ActFilesSchema]
    smetafiles: List[SmetaFilesSchema]

    class Config:
        from_attributes = True

class ReferenceBookSchema(BaseModel):
    mainworks: List[MainWorksSchema]
    fixworks: List[SubWorksSchema]
    subworks: List[FixWorksSchema]

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

"""
class PaymentsILSchema(BaseModel):
    id: int
    date: datetime
    type: str
    sum: Decimal

    class Config:
        orm_mode = True

class EgrnILSchema(BaseModel):
    id: int
    date: datetime
    number: str
    file: str


class AllILDataSchema(BaseModel):
    id: int
    street: str
    house: str
    appartment: str
    accounts_il: Optional[List[AccountILSchema]]
    egrn_il: Optional[List[EgrnILSchema]]
    property_self: bool
    one_or_parts: bool
    il_number: Optional[str]
    il_date: Optional[datetime]
    ur_in_work: bool
    gov_tax: Optional[Decimal]
    order_cancel: bool
    bailiff_forward_date: Optional[datetime]
    start_exec_pross_date: Optional[datetime]
    sum_all_get: Optional[Decimal]
    sum_not_yet_get: Optional[Decimal]
    payments: Optional[Decimal]
    payments_il: Optional[List[PaymentsILSchema]]
    debt_sum: Optional[Decimal]
    notes: Optional[str]

    class Config:
        orm_mode = True"""