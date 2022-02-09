from operator import contains
from fastapi import Form
from typing import Optional

async def decode_string_from_latin(string: str):
    return string.encode('Latin-1').decode('utf-8')

async def decode_address_data_to_db_params(addresses_str):
    params_list = addresses_str.split('; ')
    params_result_list = []
    for params in params_list:
        params_buf = {}
        params_buf['part_size'] = None
        for indx, param in enumerate(params.split(', ')):
            if indx == 0:
                params_buf['address_id'] = int(param)
                continue
            if indx == 1:
                params_buf['full_owner'] = bool(param)
                continue
            if indx == 2:
                params_buf['part_owner'] = bool(param)
                continue
            if indx == 3 and param != 'null':
                params_buf['part_size'] = param
        params_result_list.append(params_buf)        
    return params_result_list

async def decode_organisations_data_to_db_params(organisations_str):
    return organisations_str.split('; ')




async def contact_address_decode_depends(
    street: str = Form(...),
    house_number: str = Form(...),
    entrance: str = Form(...),
    appartment: str = Form(...)
):
    return {
        'street': await decode_string_from_latin(street),
        'house_number': await decode_string_from_latin(house_number),
        'entrance': await decode_string_from_latin(entrance),
        'appartment': await decode_string_from_latin(appartment),
    }

async def create_contact_organisation_decode_depends(
    full_name: str = Form(...),
    short_name: str = Form(...)
):
    return {
        'full_name': await decode_string_from_latin(full_name),
        'short_name': await decode_string_from_latin(short_name),
    }

async def create_contact_user_decode_depends(
    name: str = Form(...),
    second_name: Optional[str] = Form(None),
    surname: Optional[str] = Form(None),
    addresses: Optional[str] = Form(None),
    organisations: Optional[str] = Form(None),
    home_phones: Optional[str] = Form(None),
    work_phones: Optional[str] = Form(None),
    mobile_phones: Optional[str] = Form(None),
    emails: Optional[str] = Form(None),
    note: Optional[str] = Form(None), 
):    
    return {
        'name': await decode_string_from_latin(name),
        'second_name': await decode_string_from_latin(second_name),
        'surname': await decode_string_from_latin(surname),
        'addresses': await decode_address_data_to_db_params(addresses),
        'organisations': await decode_organisations_data_to_db_params(organisations),
        'home_phones': await decode_string_from_latin(home_phones),
        'work_phones': await decode_string_from_latin(work_phones),
        'mobile_phones': await decode_string_from_latin(mobile_phones),
        'emails': await decode_string_from_latin(emails),
        'note': await decode_string_from_latin(note),
    }