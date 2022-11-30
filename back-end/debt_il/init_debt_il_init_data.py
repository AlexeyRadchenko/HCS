#from argparse import ArgumentParser
from copy import copy
from gettext import find
from isort import file
from api.utils.utils import init_debt_il_db_data
from asyncio import get_event_loop
from openpyxl import load_workbook
from re import findall, search
from datetime import datetime
from decimal import Decimal

def get_street_house_number_and_appartment(row_data):
    address_arr = row_data.split('-')
    if len(address_arr) == 2:
        house_number_str = search('\d+\w?$', address_arr[0])
        house_number = house_number_str.group(0)
        street = address_arr[0].rstrip(house_number).strip(' ').capitalize()
        appartment = address_arr[1].strip(' ')
        return street, house_number, appartment

    if len(address_arr) != 2:
        address_arr = row_data.split(' ')
        if address_arr[-1] == 'нежилое':
            return address_arr


def get_name_secondname_surname(row_data):
    data = row_data.split(' ')
    fio_list = [string_data for string_data in data if string_data != '']
    if len(fio_list) == 3:        
        surname = fio_list[0]
        name = fio_list[1]
        second_name = fio_list[2]
        return name, second_name, surname
    return row_data, row_data, row_data

def get_pross_period(str_date):
    dates = findall(r'\d+.\d+.\d+', str_date)
    if len(dates) == 2:
        date1= dates[0] if isinstance(dates[0], datetime) else datetime.strptime(dates[0], '%d.%m.%Y')
        date2= dates[1] if isinstance(dates[1], datetime) else datetime.strptime(dates[1], '%d.%m.%Y')
        return date1, date2
    return None, None

def load_data_from_xlsx(filename):
    wb = load_workbook(filename=filename)
    sheet = wb.active
    street, house = None, None
    row_data = {}
    row_data['accounts'] = []
    data_list = []

    for index, row in enumerate(sheet.rows):
        if index >= 1:
            if row[0].value:
                if row_data.get('street'):
                    data_list.append(row_data)
                    row_data = {}
                    row_data['accounts'] = []
                street, house, appartment = get_street_house_number_and_appartment(row[0].value)
                row_data['street'] = street
                row_data['house'] = house
                row_data['appartment'] = appartment
            account = {}

            if row[1].value:   
                account['name'], account['second_name'], account['surname'] = get_name_secondname_surname(row[1].value)
                row_data['accounts'].append(account)

            if row[2].value:
                try:
                    row_data['il_date'] = row[2].value if isinstance(row[2].value, datetime) else datetime.strptime(row[2].value, '%d.%m.%Y')
                except ValueError:
                    row_data['notes'] = row[2].value
            else: 
                row_data['il_date'] = None

            if row[3].value:
                row_data['il_number'] = row[3].value   
            else:
                row_data['il_number'] = 'нет номера'

            if row[4].value:
                row_data['debt_sum_il'] = row[4].value  
            else:
                row_data['debt_sum_il'] = 0.00

            if row[5].value:
                row_data['gov_tax'] = row[5].value 
            else:
                row_data['gov_tax'] = 0.00

            if row[6].value:
                start, end = get_pross_period(row[6].value)
                row_data['start_exec_pross_date'] = start 
                row_data['end_exec_pross_date'] = end
            else:
                row_data['start_exec_pross_date'] = None
                row_data['end_exec_pross_date'] = None

            if row[7].value:
                row_data['bailiff_forward_date'] = None
                row_data['notes'] = row[7].value 
            else:
                row_data['bailiff_forward_date'] = None

            if row[8].value:
                row_data['sum_all_get'] = None
                row_data['notes'] = row[8].value  
            else:
                row_data['sum_all_get'] = None

            if row[9].value:
                if not row_data.get('notes'):
                    row_data['notes'] = ''
                row_data['notes'] = str(row_data.get('notes')) + ' ' + row[9].value 
            else:
                row_data['notes'] = None

            row_data['organisation_id'] = None               
           
    return data_list
       
if __name__ == '__main__':
    data_komf = load_data_from_xlsx('debt_il_komf.xlsx')
    #data_jks = load_data_from_xlsx('debt_il_jks.xlsx')
    loop = get_event_loop()
    loop.run_until_complete(init_debt_il_db_data(data_komf, 1))
    #loop.run_until_complete(init_debt_il_db_data(data_jks, 2))
            

    """parser = ArgumentParser(description="Create superuser for first start service")
    parser.add_argument("--login", "-l", action="store", dest='login', help="Enter superuser login", required=True)
    parser.add_argument("--password", "-p", action="store", dest='password', help="Enter superuser password", required=True)
    args = parser.parse_args()
    if args.login and args.password:
        loop = get_event_loop()
        loop.run_until_complete(init_superuser(args.login, args.password))
    if not args.password:
        print("Enter superuser password")
    if not args.login:
        print("Enter superuser login")"""
