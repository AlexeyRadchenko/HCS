from distutils.command.upload import upload
from fastapi import APIRouter, Depends, Form
from fastapi import Security, Body
from typing import List
from datetime import datetime

from sqlalchemy.ext.asyncio.session import AsyncSession
from ..security.access_depends import user_scope_authorize
from .depends import contact_address_decode_depends, create_contact_organisation_decode_depends, create_contact_user_decode_depends
from ..settings.settings import settings
from ..databese.database import get_async_session, row2dict
from ..databese.clients.schemas import (
    ContactsClientSchema, ContactsClientFullDataSchema, ContactsAddressesSchema, ContactsOrganisationsSchema, ContactsAddressesHouseStreetOrgIdScheme
    )
from ..databese.clients.crud import (
    get_contacts_clients_list, create_contacts_db_oject, get_contacts_client_by_uuid, update_contacts_client_by_uuid, get_addressess_house_street_from_db_by_org_id,
    get_address_id_by_street_house_appartment, get_client_by_name_secondname_surname, delete_contacts_client_by_uuid
    )
from ..databese.clients.models import (
    ContactsClients, ContactsOrganisations, ContactsClientsAddresses, ContactsClientOrganisations, ContactsPhones, ContactsEmails, ContactsAddresses,
    ContactsEditJournal
    )


router = APIRouter()


@router.post("/contacts_users/create_contact_address", response_model=ContactsAddressesSchema)
async def create_contact_address_handler(
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.MANAGEMENT_CONTACTS_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session),
    form_data: dict = Depends(contact_address_decode_depends)
    ):
    address = ContactsAddresses(
        street=form_data['street'], house_number=form_data['house_number'], entrance=form_data['entrance'], appartment=form_data['appartment'],
        organisation_id=form_data['organisation_id']
    )
    created_address_in_db = await create_contacts_db_oject(db_session, address)
    return created_address_in_db

@router.post("/contacts_users/create_contact_organisation", response_model=ContactsOrganisationsSchema)
async def create_contact_address_handler(
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.MANAGEMENT_CONTACTS_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session),
    form_data: dict = Depends(create_contact_organisation_decode_depends)
    ):
    
    organisation = ContactsOrganisations(
        full_name=form_data['full_name'], short_name=form_data['short_name']
    )
    created_organisation_in_db = await create_contacts_db_oject(db_session, organisation)
    return created_organisation_in_db

@router.get("/organisation/{id}/addresses_house_street", response_model=List[ContactsAddressesHouseStreetOrgIdScheme])
async def get_addresses_house_street_list_by_organisation_id(
    id: int,
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.MANAGEMENT_CONTACTS_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session)
):
    addresses = await get_addressess_house_street_from_db_by_org_id(db_session, id)
    return addresses

@router.post("/contacts_users/create_contact/", response_model=ContactsClientSchema)
async def create_contact_user_handler(
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.MANAGEMENT_CONTACTS_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session),
    form_data: dict = Depends(create_contact_user_decode_depends)
    ):

    existing_client = await get_client_by_name_secondname_surname(db_session, form_data['name'], form_data['second_name'], form_data['surname'])
    if existing_client:
        return existing_client    
    client = ContactsClients(
        name=form_data['name'], second_name=form_data['second_name'], surname=form_data['surname'], note=form_data['note']
    )
    created_client_in_db = await create_contacts_db_oject(db_session, client)

    if form_data['home_phones'] or form_data['work_phones'] or form_data['mobile_phones']:
        client_phones = ContactsPhones(
            client_uuid=created_client_in_db.uuid,
            home_phone=form_data['home_phones'],
            work_phone=form_data['work_phones'],
            mobile_phone=form_data['mobile_phones']
        )
        created_client_phones_in_db = await create_contacts_db_oject(db_session, client_phones)

    if form_data['emails']:
        client_emails_or_messengers = ContactsEmails(client_uuid=created_client_in_db.uuid, email=form_data['emails'])
        created_client_emails_or_messangers_in_db = await create_contacts_db_oject(db_session, client_emails_or_messengers)
     
    if form_data['addresses']:
        for address_data in form_data['addresses']:
            address_id = await get_address_id_by_street_house_appartment(db_session, address_data['street'], address_data['house'], address_data['appartment'])
            client_address = ContactsClientsAddresses(
                client_uuid=created_client_in_db.uuid, 
                address_id=address_id,
                full_owner=address_data['full_owner'],
                part_owner=address_data['part_owner'],
                part_size=address_data['part_size'])
            created_client_address_in_db = await create_contacts_db_oject(db_session, client_address)
            client_organisation = ContactsClientOrganisations(client_uuid=created_client_in_db.uuid, org_id=address_data['org'])
            created_cleint_organisation_in_db = await create_contacts_db_oject(db_session, client_organisation)   

    create_journal_record = ContactsEditJournal(
        client_uuid=created_client_in_db.uuid,
        who_make=form_data['system_user']
    )

    created_journal_record = await create_contacts_db_oject(db_session, create_journal_record)

    return created_client_in_db

@router.get("/contacts_users/contacts", response_model=List[ContactsClientFullDataSchema]) #
async def get_contacts_users_list(
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.MANAGEMENT_CONTACTS_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session)
    ):
    contacts_clients = await get_contacts_clients_list(db_session)
    return contacts_clients

@router.get("/contacts_users/contact/{uuid}", response_model=ContactsClientFullDataSchema)
async def get_contacts_user_data(
    uuid: str,
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.MANAGEMENT_CONTACTS_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session)
    ):
    contact = await get_contacts_client_by_uuid (db_session, uuid)
    return contact

@router.put("/contacts_users/contact/{uuid}", response_model=ContactsClientSchema)
async def update_contacts_user_data(
    uuid: str,
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.MANAGEMENT_CONTACTS_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session),
    form_data: dict = Depends(create_contact_user_decode_depends)
    ):
    update_client = ContactsClients(
        name=form_data['name'],
        second_name=form_data['second_name'],
        surname=form_data['surname'],
        note=form_data['note'] if form_data['note'] and form_data['note'] != 'undefined' else ''
    )

    client_phones = None    
    if form_data['home_phones'] or form_data['work_phones'] or form_data['mobile_phones']:
        client_phones = ContactsPhones(
            home_phone=form_data['home_phones'] if form_data['home_phones'] and form_data['home_phones'] != 'undefined' else '',
            work_phone=form_data['work_phones'] if form_data['work_phones'] and form_data['work_phones'] != 'undefined' else '',
            mobile_phone=form_data['mobile_phones'] if form_data['mobile_phones'] and form_data['mobile_phones'] != 'undefined' else ''
        )

    client_emails_or_messengers = None
    if form_data['emails']:
        client_emails_or_messengers = ContactsEmails(email=form_data['emails'])

    update_journal = ContactsEditJournal(
        who_update=form_data['system_user']
    )

    result = await update_contacts_client_by_uuid(db_session, update_client, update_journal, uuid, client_phones, client_emails_or_messengers)
    return result

@router.delete("/contacts_users/contact/{uuid}")
async def delete_contacts_user_data(
    uuid: str,
    request_body: dict = Body(...),
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.MANAGEMENT_CONTACTS_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session)
    ):
    update_journal = ContactsEditJournal(
        date_delete=datetime.now(),
        who_delete=request_body['system_user']
    )
    await delete_contacts_client_by_uuid(db_session, uuid, update_journal)
    return {'key': uuid, 'del_status': True}
    # 372d0fb3-d9ca-4f59-98c5-5e4fb25059ea

