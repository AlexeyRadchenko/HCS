from datetime import datetime
from openpyxl import load_workbook
from xlsxwriter import Workbook
from ..settings.settings import settings

async def genereate_year_act_xlsx_file(year, house, data):
    template = load_workbook(settings.YEAR_ACT_FILE_TEMPLATE_PATH + settings.YEAR_ACT_FILE_TEMPLATE_NAME)
    template_sheet = template.active
    now = datetime.now()
    act_num = 1
    house_number = data[0]['houses']['number']
    street_name = data[0]['houses']['street']
    template_sheet['A1'] = f' АКТ № {act_num}'
    template_sheet['A3'] = f' многоквартирном доме № {house_number} по улице {street_name}'
    print(year, house, data, data[0]['houses']['street'], data[0]['houses']['number'])
    # act_num, street_name, house_number
    template.save(settings.YEAR_ACT_FILE_TEMPLATE_PATH + "ready.xlsx")
    
