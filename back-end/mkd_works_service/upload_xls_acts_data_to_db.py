import openpyxl
import asyncio
from datetime import datetime
from api.utils.utils import upload_mkd_works_from_xlsx_to_db_util


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
            if isinstance(row[1], str) and row[1].strip(' ') == 'ИТОГО':
                count +=1
                house_address = None
                continue
            if row[1] == None:
                continue
            #print('pr1',row)
            if not isinstance(row[1], datetime):
                print("NOT DATETIME", row[1])
            if not house_address:
                house_address = row[0]   
            row_dict = {
                'Адрес дома': house_address, 
                'Месяц и год проведения работ': row[1], 
                'Номер работы по справочнику': row[2], 
                'Нименование работы': row[3], 
                'Периодичность': row[4], 
                'номер сметы': row[5], 
                'Цена выполненной работы (оказанной услуги) в рублях': row[6], 
                'еденицы измерения': row[7],
            }
            all_data.append(row_dict)
        #print(count)
        count = 0
    
    return all_data
async def main():
    file_path = "house_works_accum.xlsx"  # Укажите путь к вашему файлу
    data = process_xlsx(file_path)
    await upload_mkd_works_from_xlsx_to_db_util(data, 1) #загрузка для комфорта


if __name__ == "__main__":
    asyncio.run(main())

    