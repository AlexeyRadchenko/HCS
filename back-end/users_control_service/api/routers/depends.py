from operator import contains
from fastapi import Form
from typing import Optional

async def decode_string_from_latin(string: str):
    try:
        dec_str = string.encode('Latin-1').decode('utf-8')
        return dec_str
    except (UnicodeEncodeError, AttributeError):
        return string

async def decode_address_data_to_db_params(street_house, entrance, appartment, part_own):
    params_list = street_house.split(' - ')
    street = params_list[0]
    try:
        house, organisation = params_list[1].split('_')
    except ValueError:
        house = params_list[1]
        organisation = ''
    if part_own == '1':
        full_owner = True
        part_owner = False
    if part_own and part_own !='1':
        full_owner = False
        part_owner = True
    return [
        {
            'street': street,
            'house': house,
            'entrance': entrance,
            'appartment': appartment,
            'org': organisation,
            'full_owner': full_owner,
            'part_owner': part_owner,
            'part_size': part_own
        }
    ]    
    

async def decode_organisations_data_to_db_params(organisations_str):
    return organisations_str.split('; ')


async def contact_address_decode_depends(
    street: str = Form(...),
    house_number: str = Form(...),
    entrance: str = Form(...),
    appartment: str = Form(...),
    organisation_id: str = Form(...)
):
    return {
        'street': await decode_string_from_latin(street),
        'house_number': await decode_string_from_latin(house_number),
        'entrance': await decode_string_from_latin(entrance),
        'appartment': await decode_string_from_latin(appartment),
        'organisation_id': await decode_string_from_latin(organisation_id),
    }

async def create_contact_organisation_decode_depends(
    full_name: str = Form(...),
    short_name: str = Form(...)
):
    return {
        'full_name': await decode_string_from_latin(full_name),
        'short_name': await decode_string_from_latin(short_name),
    }

async def create_management_user_decode_depends(
    username: str = Form(...),
    password: str = Form(...)
):  
    return {
        'username': await decode_string_from_latin(username),
        'password': await decode_string_from_latin(password)
    }

async def create_account_user_decode_depends(
    username: str = Form(...),
    password: str = Form(...),
    street: str = Form(...),
    house: str = Form(...),
    appartment: str = Form(...)
):  
    return {
        'username': await decode_string_from_latin(username),
        'password': await decode_string_from_latin(password),
        'street': await decode_string_from_latin(street),
        'house': await decode_string_from_latin(house),
        'appartment': await decode_string_from_latin(appartment),
    }