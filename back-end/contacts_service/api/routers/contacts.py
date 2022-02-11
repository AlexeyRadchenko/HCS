from fastapi import APIRouter, Depends, Form
from fastapi import Security
from typing import List

from sqlalchemy.ext.asyncio.session import AsyncSession
from ..security.access_depends import user_scope_authorize
from .depends import contact_address_decode_depends, create_contact_organisation_decode_depends, create_contact_user_decode_depends
from ..settings.settings import settings
from ..databese.database import get_async_session, contacts_obj_list_to_dicts_list
from ..databese.clients.schemas import ContactsClientSchema, ContactsClientFullDataSchema, ContactsAddressSchema, ContactsOrganisationsSchema
from ..databese.clients.crud import get_contacts_clients, create_contacts_db_oject
from ..databese.clients.models import (
    ContactsClients, ContactsAddress, ContactsOrganisations, ContactsClientsAddress, ContactsClientOrganisations, ContactsPhones, ContactsEmails
    )


router = APIRouter()


@router.post("/contacts_users/create_contact_address", response_model=ContactsAddressSchema)
async def create_contact_address_handler(
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.MANAGEMENT_CONTACTS_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session),
    form_data: dict = Depends(contact_address_decode_depends)
    ):
    address = ContactsAddress(
        street=form_data['street'], house_number=form_data['house_number'], entrance=form_data['entrance'], appartment=form_data['appartment']
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
  

@router.post("/contacts_users/create_contact", response_model=ContactsClientSchema)
async def create_contact_user_handler(
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.MANAGEMENT_CONTACTS_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session),
    form_data: dict = Depends(create_contact_user_decode_depends)
    ):

    phones_id = None
    emails_or_messangers_id = None
    addresses = None
    organisations = None

    if form_data['home_phones'] or form_data['work_phones'] or form_data['mobile_phones']:
        client_phones = ContactsPhones(
            home_phone=form_data['home_phones'], work_phone=form_data['work_phones'], mobile_phone=form_data['mobile_phones']
            )
        created_client_phones_in_db = await create_contacts_db_oject(db_session, client_phones)
        phones_id = created_client_phones_in_db.id

    if form_data['emails']:
        client_emails_or_messengers = ContactsEmails(email=form_data['emails'])
        created_client_emails_or_messangers_in_db = await create_contacts_db_oject(db_session, client_emails_or_messengers)
        emails_or_messangers_id = created_client_emails_or_messangers_in_db.id

    user = ContactsClients(
        name=form_data['name'], second_name=form_data['second_name'], surname=form_data['surname'], phones=phones_id,
        emails=emails_or_messangers_id, note=form_data['note']
    )
    created_user_in_db = await create_contacts_db_oject(db_session, user)
    
    if form_data['addresses']:
        addresses = []
        for address_data in form_data['addresses']:
            client_address = ContactsClientsAddress(
                client_uuid=created_user_in_db.uuid, 
                address_id=address_data['address_id'],
                full_owner=address_data['full_owner'],
                part_owner=address_data['part_owner'],
                part_size=address_data['part_size'])
            created_client_address_in_db = await create_contacts_db_oject(db_session, client_address)
            addresses.append(created_client_address_in_db)

    if form_data['organisations']:
        organisations = []
        for organisation in form_data['organisations']:
            client_organisation = ContactsClientOrganisations(client_uuid=created_user_in_db.uuid, org_id=organisation)
            created_cleint_organisation_in_db = await create_contacts_db_oject(db_session, client_organisation)
            organisations.append(created_cleint_organisation_in_db)

    #created_user_in_db.addresses=addresses
    #created_user_in_db.organisations=organisations
    return created_user_in_db

@router.get("/contacts_users/contacts", response_model=List[ContactsClientFullDataSchema])
async def get_contacts_users_list(
    #user_auth: bool = Security(user_scope_authorize, scopes=[settings.MANAGEMENT_SCOPE])
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.MANAGEMENT_CONTACTS_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session)
    ):
    contacts_clients = await get_contacts_clients(db_session)
    #print(contacts_clients)
    #print(contacts_obj_list_to_dicts_list(contacts_clients))
    result_clients = [contact[0] for contact in contacts_clients]
    print(result_clients)
    print(result_clients[0].address)
    return result_clients