from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Any
from pydantic import BaseModel
from uuid import UUID

class PassportILSchema(BaseModel):
    id: Optional[int]
    seria: Optional[str]
    number: Optional[str]
    who_take: Optional[str]
    when_take: Optional[datetime]
    squad_code: Optional[str]
    birth_date: Optional[datetime]
    birth_city: Optional[str]
    scan: Optional[str]

    class Config:
        orm_mode = True

class AccountILSchema(BaseModel):
    uuid: UUID
    account_number: str
    name: str
    second_name: str
    surname: str
    passport_il: Optional[PassportILSchema]

    class Config:
        orm_mode = True

class PaymentsILSchema(BaseModel):
    id: int
    date: datetime
    type: str
    sum: Decimal

    class Config:
        orm_mode = True


class AllILDataSchema(BaseModel):
    id: int
    street: str
    house: str
    appartment: str
    accounts_il: Optional[List[AccountILSchema]]
    property_self: bool
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
