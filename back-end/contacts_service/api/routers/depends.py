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

async def create_contact_user_decode_depends(
    name: str = Form(...),
    second_name: Optional[str] = Form(None),
    surname: Optional[str] = Form(None),
    street_house: Optional[str] = Form(None),
    entrance: Optional[str] = Form(None),
    appartment: Optional[str] = Form(None),
    part_own: Optional[str] = Form(None),
    home_phones: Optional[str] = Form(None),
    work_phones: Optional[str] = Form(None),
    mobile_phones: Optional[str] = Form(None),
    emails: Optional[str] = Form(None),
    note: Optional[str] = Form(None),
    system_user: Optional[str] = Form(None)
):  
    print()
    return {
        'name': await decode_string_from_latin(name),
        'second_name': await decode_string_from_latin(second_name),
        'surname': await decode_string_from_latin(surname),
        'addresses': await decode_address_data_to_db_params(street_house, entrance, appartment, part_own),
        'home_phones': await decode_string_from_latin(home_phones),
        'work_phones': await decode_string_from_latin(work_phones),
        'mobile_phones': await decode_string_from_latin(mobile_phones),
        'emails': await decode_string_from_latin(emails),
        'note': await decode_string_from_latin(note),
        'system_user': await decode_string_from_latin(system_user),
    }
