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

class WaterCounterSchema(BaseModel):
    id: int
    outer_base_id: int
    setup_date: datetime
    in_work: bool
    serial_number: Optional[str]
    data: Decimal
    old_data: Decimal
    diff: Decimal
    date_update: datetime
    who_last_modify: Optional[str]

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
    water_counters: Optional[List[WaterCounterSchema]]
    gas_counters: Optional[List[GasCounterSchema]]
    account_params: Optional[AccountParamsSchema] 
    account_summary: Optional[AccountSummarySchema]

    class Config:
        orm_mode = True    
