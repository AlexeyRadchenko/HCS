#from argparse import ArgumentParser
from copy import copy
from gettext import find
from isort import file
from api.utils.utils import init_contacts_db_data
from asyncio import get_event_loop
from openpyxl import load_workbook
from re import findall

def get_street_and_house_number(row_data):
    street, house = row_data.split(',')
    street = street.replace('дом', '')
    return street.strip(), house.strip()

def get_appartment_number_and_owner(row_data):
    full_owner = False
    part_owner = False
    part_size = ''
    if '/' in row_data:
        part_owner = True
        part_size = 'указать размер доли'
        appartment = row_data.split('/')[0]
        return appartment, full_owner, part_owner, part_size
    full_owner = True
    return row_data, full_owner, part_owner, part_size

def get_name_secondname_surname(row_data):
    data = row_data.split(' ')
    fio_list = [string_data for string_data in data if string_data != '']
    if len(fio_list) == 3:        
        surname = fio_list[0]
        name = fio_list[1]
        second_name = fio_list[2]
        return name, second_name, surname
    return row_data, '', ''

def get_home_mobile_work_phone_from_row(row_data):
    MOBILE_PHONE_REG = r'((?:\+\d{2}[-\.\s]??|\d{4}[-\.\s]??)?(?:\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}))'
    HOME_PHONE_REG = r'^\d[-\.\s]\d{2}-\d{2}\s?'
    try:
        row_d = row_data[3].value
    except IndexError:
        return 'break' ,'', '', ''
    if not row_d:
        return '', '', '', ''
    home_numbers = findall(HOME_PHONE_REG, row_d)
    mob_numbers = findall(MOBILE_PHONE_REG, row_d)
    work_numbers = []
    note = row_d
    return home_numbers, mob_numbers, work_numbers, note
    


def load_data_from_xlsx(filename):
    wb = load_workbook(filename=filename)
    sheet = wb.active
    street, house = None, None
    data_list = []
    
    for index, row in enumerate(sheet.rows):
        if index >= 2:
            if not row[1].value and row[0].value != '<>':
                row_data = {}
                street, house = get_street_and_house_number(row[0].value)
                row_data['street'] = street
                row_data['house'] = house
                continue
            row_data['name'], row_data['second_name'], row_data['surname'] = get_name_secondname_surname(row[0].value)
            row_data['entrance'] = row[2].value
            appartment = str(row[1].value)
            if appartment and appartment.lower() == 'пени':
                continue
            if appartment:
                row_data['appartment'], row_data['full_owner'], row_data['part_owner'], row_data['part_size'] = get_appartment_number_and_owner(appartment)
            row_data['home_phones'], row_data['mobile_phones'], row_data['work_phones'], row_data['note'] = get_home_mobile_work_phone_from_row(row)
            if row_data['home_phones'] == 'break':
                break
            clear_var = copy(row_data)
            data_list.append(clear_var)
            clear_var = None
    return data_list
       
if __name__ == '__main__':
    print("DON'T FORGET DEL DATE_CREATE FOR SQLITE IN INIT_CONTACTS_DB_DATA")
    data_komf = load_data_from_xlsx('jf_komf.xlsx')
    data_jks = load_data_from_xlsx('jf_jks.xlsx')
    loop = get_event_loop()
    loop.run_until_complete(init_contacts_db_data(data_komf, 1))
    loop.run_until_complete(init_contacts_db_data(data_jks, 2))
            

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
