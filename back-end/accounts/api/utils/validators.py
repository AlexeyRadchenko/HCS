from decimal import Decimal, InvalidOperation
from datetime import datetime

def valid_counter_data(data):
    try:
        d_data = Decimal(data)
        return True, d_data 
    except InvalidOperation:
        return False, data

def valid_data_date(old):
    try:
        old_date = datetime.strptime(old, '%Y-%m-%dT%H:%M:%S')
    except ValueError:
        return False, None
    now = datetime.now()
    if old_date.month != now.month:
        return True, old_date
    else:
        return False, None
