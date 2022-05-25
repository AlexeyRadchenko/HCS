from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Any
from pydantic import BaseModel

class AddressSchema(BaseModel):
    id: int
    street: str
    house: str
    entrance: str
    appartment: str
    org_id: Optional[int]

    class Config:
        orm_mode = True

class ElectricCounterSchema(BaseModel):
    id: int
    outer_base_id: int
    setup_date: Optional[datetime]
    in_work:bool
    type: str
    serial_number: Optional[str]
    simple_data: Optional[int]
    day_data: Optional[int]
    night_data: Optional[int]
    old_simple_data: Optional[int]
    old_day_data: Optional[int]
    old_night_data: Optional[int]
    simple_diff: Optional[int]
    day_diff: Optional[int]
    night_diff: Optional[int]
    date_update: Optional[datetime]
    last_date_update: Optional[datetime]
    who_last_modify: str

    class Config:
        orm_mode = True

class WaterCounterSchema(BaseModel):
    id: int
    outer_base_id: int
    setup_date: Optional[datetime]
    in_work: bool
    type: Optional[str]
    serial_number: Optional[str]
    data: Decimal
    old_data: Decimal
    diff: Optional[Decimal]
    date_update: Optional[datetime]
    last_date_update: Optional[datetime]
    who_last_modify: str

    class Config:
        orm_mode = True

class GasCounterSchema(WaterCounterSchema):
    class Config:
        orm_mode = True
    
class AccountParamsSchema(BaseModel):
    id: int
    etc: Optional[str]
    sum_square: Optional[Decimal]
    living_square: Optional[Decimal]
    living_quantity: Optional[Decimal]
    record_living_quantity: Optional[int]
    account_id: int

    class Config:
        orm_mode = True

class AccountSummarySchema(BaseModel):
    id: int
    doc_date: datetime
    payment_sum: Decimal
    debt_start_period: Decimal
    debt: Decimal
    paying: Decimal
    last_payment_date: datetime
    debt_end_period: Decimal
    ending_payment: Decimal
    account_id: int

    class Config:
        orm_mode = True

class AccountSchema(BaseModel):
    id: int
    account: str
    name: Optional[str]
    second_name: Optional[str]
    surname: Optional[str]
    address_id: int
    address: AddressSchema
    electric_counters: Optional[List[ElectricCounterSchema]]
    water_counters: Optional[List[WaterCounterSchema]]
    gas_counters: Optional[List[GasCounterSchema]]
    account_params: Optional[AccountParamsSchema] 
    account_summary: Optional[AccountSummarySchema]

    class Config:
        orm_mode = True

class AccountWaterCounterSchema(BaseModel):
    account: str
    water_counters: Optional[List[WaterCounterSchema]]

    class Config:
        orm_mode = True

class OrganisationSchema(BaseModel):
    id: int
    short_name: str
    full_name: str
    address: str
    phones: str
    dispatcher_phones: Optional[str]
    site: Optional[str]
    r_s: Optional[str]
    bank: str
    bik: str
    inn: str
    kpp: str
    qr_short_name: str
    korr_acc: str

    class Config:
        orm_mode = True