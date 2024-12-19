from fastapi import Form
from typing import Optional, List
from decimal import Decimal
from json import loads


async def depends_create_il_list_with_accounts(
    street: str = Form(...),
    house: str = Form(...),
    appartment: str = Form(...),
    one_or_parts: bool = Form(...),
    property_self: bool = Form(...),
    uk_org: int = Form(...),
    il_number: str = Form(...),
    il_date: str = Form(...),
    gov_tax: Optional[Decimal] = Form(None),
    sum_all_get: Optional[Decimal] = Form(None),
    sum_not_yet_get: Optional[Decimal] = Form(None),
    debt_sum_il: Optional[Decimal] = Form(None),
    period: Optional[List[str]] = Form(None),
    accounts_il: List[str] = Form(...)
):  
    return {
        'street': street,
        'house': house,
        'appartment': appartment,
        'one_or_parts': one_or_parts,
        'property_self': property_self,
        'uk_org': uk_org,
        'il_number': il_number,
        'il_date': il_date,
        'gov_tax': gov_tax,
        'sum_all_get': sum_all_get,
        'sum_not_yet_get': sum_not_yet_get,
        'debt_sum_il': debt_sum_il,
        'period': period,
        'accounts_il': [loads(acc_data) for acc_data in accounts_il if acc_data != '[object Object]']
    }

async def depends_update_il_list_with_accounts(
    id: int = Form(...), 
    street: str = Form(...),
    house: str = Form(...),
    appartment: str = Form(...),
    one_or_parts: bool = Form(...),
    property_self: bool = Form(...),
    uk_org: int = Form(...),
    il_number: str = Form(...),
    il_date: str = Form(...),
    gov_tax: Optional[Decimal] = Form(None),
    sum_all_get: Optional[Decimal] = Form(None),
    sum_not_yet_get: Optional[Decimal] = Form(None),
    debt_sum_il: Optional[Decimal] = Form(None),
    period: Optional[List[str]] = Form(None),
    accounts_il: List[str] = Form(...)
):  
    return {
        'id': id,
        'street': street,
        'house': house,
        'appartment': appartment,
        'one_or_parts': one_or_parts,
        'property_self': property_self,
        'uk_org': uk_org,
        'il_number': il_number,
        'il_date': il_date,
        'gov_tax': gov_tax,
        'sum_all_get': sum_all_get,
        'sum_not_yet_get': sum_not_yet_get,
        'debt_sum_il': debt_sum_il,
        'period': period,
        'accounts_il': [loads(acc_data) for acc_data in accounts_il if acc_data != '[object Object]']
    }