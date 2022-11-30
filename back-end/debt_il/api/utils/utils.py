from datetime import datetime
from ..database.debt_il.crud import create_debt_il_object
from ..database.debt_il.models import Organisations_il, Accounts_il, All_il, IL_accounts
from ..database.database import async_session

async def init_debt_il_db_data(obj_list, org):
    async with async_session() as db_session:

        if org == 1:
            organisation_obj = Organisations_il (
                full_name='ООО "Комфортный дом"',
                short_name='Комфортный дом'
            )
        if org == 2:
            organisation_obj = Organisations_il (
                full_name='ООО "ЖилКомСервис - Трехгорный"',
                short_name='ЖКС - Трехгорный'
            )

        organisation = await create_debt_il_object(db_session, organisation_obj)
        org = organisation.id

        for data in obj_list:
            list_il_obj = All_il(
                street=data['street'],
                house=data['house'],
                appartment=data['appartment'],
                il_number=data['il_number'],
                il_date=data['il_date'],
                gov_tax=data['gov_tax'],
                bailiff_forward_date=data['bailiff_forward_date'],
                start_exec_pross_date=data['start_exec_pross_date'],
                end_exec_pross_date=data['end_exec_pross_date'],
                sum_all_get=data['sum_all_get'],
                debt_sum_il=data['debt_sum_il'],
                notes=data['notes'],
                organisation_id=org
            )

            list_il = await create_debt_il_object(db_session, list_il_obj)

            for account in data['accounts']:
                account_il_obj = Accounts_il(
                    name=account['name'],
                    second_name=account['second_name'], 
                    surname=account['second_name'],
                )

                account_il = await create_debt_il_object(db_session, account_il_obj)

                il_account_obj = IL_accounts(
                    il_id=list_il.id,
                    account_uuid=account_il.uuid
                )

                await create_debt_il_object(db_session, il_account_obj)

