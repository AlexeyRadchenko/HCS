from datetime import datetime
from http import client
from ..databese.clients.crud import create_contacts_db_oject
from ..databese.database import get_async_session
from ..databese.clients.models import ContactsClients, ContactsAddresses, ContactsClientsAddresses, ContactsEditJournal, ContactsClientOrganisations, ContactsOrganisations, ContactsPhones
from ..databese.database import async_session

async def init_contacts_db_data(obj_list, org):
    async with async_session() as db_session:

        if org == 1:
            organisation_obj = ContactsOrganisations (
                full_name='ООО "Комфортный дом"',
                short_name='Комфортный дом'
            )
        if org == 2:
            organisation_obj = ContactsOrganisations (
                full_name='ООО "ЖилКомСервис - Трехгорный"',
                short_name='ЖКС - Трехгорный'
            )

        organisation = await create_contacts_db_oject(db_session, organisation_obj)
        
        for data in obj_list:
            contact_obj = ContactsClients(
                name=data['name'],
                second_name=data['second_name'],
                surname=data['surname'],
                note=data['note']
            )
            contact = await create_contacts_db_oject(db_session, contact_obj)
            address_obj = ContactsAddresses(
                street=data['street'],
                house_number=data['house'],
                entrance=data['entrance'],
                appartment=data['appartment'],
                organisation_id=org
            )
            address = await create_contacts_db_oject(db_session, address_obj)
            client_address_obj = ContactsClientsAddresses(
                client_uuid=contact.uuid,
                address_id=address.id,
                full_owner=data['full_owner'],
                part_owner=data['part_owner'],
                part_size=data['part_size']
            )
            client_address = await create_contacts_db_oject(db_session, client_address_obj)

            client_phones_obj = ContactsPhones(
                client_uuid=contact.uuid,
                home_phone=' '.join(data['home_phones']),
                mobile_phone=' '.join(data['mobile_phones']),
                work_phone=' '.join(data['work_phones'])
            )
            client_phones = await create_contacts_db_oject(db_session, client_phones_obj)

            journal_obj = ContactsEditJournal (
                client_uuid = contact.uuid,
                date_create = datetime.now(), #for sqlite del for postgresql
                who_make='admin'
            )
            journal_rec = await create_contacts_db_oject(db_session, journal_obj)

            
            client_org_obj = ContactsClientOrganisations(
                client_uuid = contact.uuid,
                org_id=org
            )
            client_org = await create_contacts_db_oject(db_session, client_org_obj)
    print("data upload to db")
    