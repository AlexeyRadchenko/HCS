from fastapi import Form
from typing import Optional


async def decode_string_from_latin(string: str):
    try:
        dec_str = string.encode('Latin-1').decode('utf-8')
        return dec_str
    except (UnicodeEncodeError, AttributeError):
        return string

async def counter_data_form_depend(
    counter_id: str = Form(...),
    counter_data: str = Form(...),
    old_counter_data: str = Form(...),
    old_date_update: str = Form(...),
    
):  
    return {
        'counter_id': await decode_string_from_latin(counter_id),
        'counter_data': await decode_string_from_latin(counter_data),
        'old_counter_data': await decode_string_from_latin(old_counter_data),
        'old_date_update': await decode_string_from_latin(old_date_update),
    }

async def counter_electric_data_form_depend(
    counter_id: str = Form(...),
    counter_simple_data: Optional[str] = Form(None),
    counter_day_data: Optional[str] = Form(None),
    counter_night_data: Optional[str] = Form(None),
    old_counter_simple_data: Optional[str] = Form(None),
    old_counter_day_data: Optional[str] = Form(None),
    old_counter_night_data: Optional[str] = Form(None),
    old_date_update: str = Form(...),
    type: str = Form(...)
    
):  
    return {
        'counter_id': await decode_string_from_latin(counter_id),
        'counter_simple_data': await decode_string_from_latin(counter_simple_data),
        'counter_day_data': await decode_string_from_latin(counter_day_data),
        'counter_night_data': await decode_string_from_latin(counter_night_data),
        'old_counter_simple_data': await decode_string_from_latin(old_counter_simple_data),
        'old_counter_day_data': await decode_string_from_latin(old_counter_day_data),
        'old_counter_night_data': await decode_string_from_latin(old_counter_night_data),
        'old_date_update': await decode_string_from_latin(old_date_update),
        'type': await decode_string_from_latin(type),
    }    