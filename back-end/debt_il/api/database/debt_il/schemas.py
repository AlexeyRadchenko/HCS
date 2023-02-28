from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Any
from pydantic import BaseModel
from uuid import UUID
from fastapi import UploadFile, File

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
    inn: Optional[str]
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
    id: Optional[int]
    date: Optional[datetime]
    number: Optional[str]
    name: Optional[str]
    file: Optional[str]
    note: Optional[str]
    del_mark: Optional[bool]
    il_id: Optional[int]

    class Config:
        orm_mode = True


class AllILDataSchema(BaseModel):
    id: int
    street: str
    house: str
    appartment: str
    accounts_il: Optional[List[AccountILSchema]]
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

class EGRNDocFileSchema(BaseModel):
    file_name: Optional[str]
    file_path: str

class PaymentUploadData(BaseModel):
    date: Optional[str]
    type:Optional[str]
    sum: Optional[str]
    il:Optional[str]
    account_name:Optional[str]
    company:Optional[str]

class PaymentUploadDataListSchema(BaseModel):
    data: List[PaymentUploadData]
   

class AccaountDataForCreatePassportData(BaseModel):
    seria: Optional[str]
    number: Optional[str]
    who_take: Optional[str]
    when_take: Optional[str]
    squad_code: Optional[str]
    birth_date: Optional[str]
    birth_place: Optional[str]
    #uploadFiles: Optional[List[UploadFile]]

class AccountDataForCreate(BaseModel):
    account_number: Optional[str]
    name: Optional[str]
    second_name: Optional[str]
    surname: Optional[str]
    inn: Optional[str]
    passport_il:  Optional[AccaountDataForCreatePassportData]

class DebtILListCreateSchema(BaseModel):
    street: str
    home: str
    appartment: str
    one_or_parts: bool
    property_self: bool
    il_number: str
    il_date: str
    gov_tax: Optional[str]
    sum_all_get: Optional[str]
    sum_not_yet_get: Optional[str]
    debt_sum_il: Optional[str]
    period: Optional[List]
    accounts_il: Optional[List[AccountDataForCreate]]