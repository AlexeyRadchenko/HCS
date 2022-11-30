from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Any
from pydantic import BaseModel
from uuid import UUID

class PassportILSchema(BaseModel):
    id: Optional[int]
    serial: Optional[str]
    number: Optional[str]
    who_take: Optional[str]
    when_take: Optional[datetime]
    squad_code: Optional[str]
    birth_date: Optional[datetime]
    birth_place: Optional[str]
    scan: Optional[str]

    class Config:
        orm_mode = True

class AccountILSchema(BaseModel):
    uuid: UUID
    account_number: Optional[str]
    name: Optional[str]
    second_name: Optional[str]
    surname: Optional[str]
    part_of_appartment: Optional[str]
    passport_il: Optional[PassportILSchema]

    class Config:
        orm_mode = True

class PaymentsILSchema(BaseModel):
    id: int
    date: datetime
    type: str
    sum: Decimal
    account_il: Optional[AccountILSchema]
    notes: Optional[str]

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
        orm_mode = True
