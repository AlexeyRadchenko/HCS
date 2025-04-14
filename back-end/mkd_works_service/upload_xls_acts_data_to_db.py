import openpyxl
import asyncio
from datetime import datetime
from api.utils.utils import upload_mkd_works_from_xlsx_to_db_util
import re


def validate(data):
    house_address = data.get('Адрес дома')
    if house_address:
        # Проверяем, что адрес дома не пустой
        if not isinstance(house_address, str) or not house_address.strip():
            raise ValueError("Адрес дома не может быть пустым", data)
        
    work_moth = data.get('Месяц и год проведения работ')
    if work_moth:
        # Проверяем, что дата в формате 'YYYY-MM-DD'
        if not isinstance(work_moth, datetime):
            pattern = r'^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0-2])\.(19|20)\d{2}$'
            if not re.match(pattern, work_moth):
                raise ValueError(f"'{work_moth}' не соответствует шаблону dd.mm.yyyy", data)
    else:
        raise ValueError("Месяц и год проведения работ не указан", data) 

    reference_num = data.get('Разд. Справ')
    if reference_num:
        pattern = r'^\d{1,2}.(\d{1,2}.)?$'
        if not re.match(pattern, reference_num):
            raise ValueError(f"{reference_num}' не соответствует шаблону", data)       
    else:
        raise ValueError("Раздел. Справочника не указан", data)
        
    reference_num_with_text = data.get('Нименование работы(услуги)')
    if reference_num_with_text:
        pattern = r'^\d{1,2}.(\d{1,2}.)?\s.+$'
        if not re.match(pattern, reference_num_with_text):
            raise ValueError(f"'{reference_num_with_text}' не соответствует шаблону", data)
    else:
        raise ValueError("Нименование работы(услуги) не указан", data)

    quantity = data.get('Кол-во единиц измерений')
    if quantity:
        # Проверяем, что количество является числом
        try:
            float(quantity)
        except ValueError:
            raise ValueError(f"Неверный формат Кол-во единиц измерений: {quantity}. Ожидается число.", data)
    else:
        raise ValueError("Кол-во единиц измерений не указан", data)    

    cost = data.get('Стоимость оказанной услуги за единицу, руб/м2')
    if cost:
        # Проверяем, что стоимость является числом
        try:
            float(cost)
        except ValueError:
            raise ValueError(f"Неверный формат стоимости: {cost}. Ожидается число.", data)  
    else:
        raise ValueError("Стоимость оказанной услуги за единицу, руб/м2 не указан", data)

    sum = data.get('Цена выполненной работы (оказанной услуги) в рублях')
    if sum:
        # Проверяем, что стоимость является числом
        try:
            float(sum)
        except ValueError:
            raise ValueError(f"Неверный формат стоимости: {sum}. Ожидается число.", data)  
    else:
        raise ValueError("Цена выполненной работы (оказанной услуги) в рублях не указан", data)


def process_xlsx(file_path):
    # Открываем xlsx файл
    wb = openpyxl.load_workbook(file_path)
    sheet_names = wb.sheetnames

    # Список для хранения всех словарей
    all_data = []

    # Итерируемся по листам, кроме последнего
    for sheet_name in sheet_names[:-1]:
        sheet = wb[sheet_name]

        # Создаём словарь для каждой строки данных
        count = 0
        house_address = None
        #print(sheet_name)
        for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row, values_only=True):
            if isinstance(row[1], str) and row[5].strip(' ') == 'ИТОГО':
                count +=1
                house_address = None
                continue
            if row[1] == None:
                count +=1
                continue
            #print('pr1',row)
            if not isinstance(row[1], datetime):
                print("NOT DATETIME", row[1])
            if not house_address:
                house_address = row[0]
            row_dict = {
                'Адрес дома': house_address, 
                'Месяц и год проведения работ': row[1],
                'Номер сметы': row[2],
                'Разд. Справ': str(row[3]),
                'Нименование работы(услуги)': row[4],
                'Периодичность': row[5],
                'Кол-во единиц измерений': row[6],
                'Стоимость оказанной услуги за единицу, руб/м2': row[7],
                'Цена выполненной работы (оказанной услуги) в рублях': row[8],
                'коментарий': row[9],
            }
            validate(row_dict)
            all_data.append(row_dict)
        #print("COUNT!@@@@@@@@@@@@@@@@@", count)
        count = 0
    
    return all_data
async def main():
    file_path = "/home/bers/HSCUploads/mks_works/свод_работ_по домам для актов 1.xlsx" #"house_works_accum.xlsx"  # Укажите путь к вашему файлу
    data = process_xlsx(file_path)
    #print("DATA@@@@@@@@@@@@@@@@@@@@@@@", len(data))
    await upload_mkd_works_from_xlsx_to_db_util(data, 1) #загрузка для комфорта


if __name__ == "__main__":
    asyncio.run(main())

    