from audioop import add
from http import client
import imp
from operator import contains
from pydoc import cli
from fastapi import APIRouter, Depends, Form
from fastapi import Security

from sqlalchemy.ext.asyncio.session import AsyncSession
from ..security.access_depends import user_scope_authorize
from ..settings.settings import settings
from ..databese.database import get_async_session
from ..databese.clients.schemas import ContactsClientSchema, ContactsCientFullDataSchema, ContactsAddressSchema, ContactsOrganisationsSchema
from ..databese.clients.crud import get_contacts_clients, create_contacts_user, create_contacts_address
from ..databese.clients.models import ContactsClients, ContactsAddress, ContactsOrganisations

router = APIRouter()


@router.post("/contacts_users/create_contact_address", response_model=ContactsAddressSchema)
async def create_contact_address_handler(
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.MANAGEMENT_CONTACTS_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session),
    street: str = Form(...),
    house_number: str = Form(...),
    entrance: str = Form(...),
    appartment: str = Form(...)
    ):
    street = street.encode('Latin-1').decode('utf-8')
    address = ContactsAddress(
        street=street, house_number=house_number, entrance=entrance, appartment=appartment
    )
    created_address_in_db = await create_contacts_address(db_session, address)
    return created_address_in_db

@router.post("/contacts_users/create_contact_organisation", response_model=ContactsOrganisationsSchema)
async def create_contact_address_handler(
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.MANAGEMENT_CONTACTS_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session),
    full_name: str = Form(...),
    short_name: str = Form(...)
    ):
    full_name = full_name.encode('Latin-1').decode('utf-8')
    short_name = short_name.encode('Latin-1').decode('utf-8')
    organisation = ContactsOrganisations(
        full_name=full_name, short_name=short_name
    )
    created_organisation_in_db = await create_contacts_address(db_session, organisation)
    return created_organisation_in_db    
  

@router.post("/contacts_users/create_contact", response_model=ContactsClientSchema)
async def create_contact_user_handler(
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.MANAGEMENT_CONTACTS_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session),
    name: str = Form(...),
    second_name: str = Form(...),
    surname: str = Form(...),
    phones: str = Form(...),
    emails: str = Form(...),
    note: str = Form(...) 
    ):
    print(name, second_name, phones, emails, note)
    user = ContactsClients(
        name=name, second_name=second_name, surname=surname, phones=phones, emails=emails, note=note
    )
    created_user_in_db = await create_contacts_user(db_session, user)
    contact = ContactsCientFullDataSchema(created_user_in_db)
    return contact

@router.get("/contacts_users/contact", response_model=ContactsCientFullDataSchema)
async def get_contacts_users_list(
    #user_auth: bool = Security(user_scope_authorize, scopes=[settings.MANAGEMENT_SCOPE])
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.MANAGEMENT_CONTACTS_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session)
    ):
    contacts_clients = get_contacts_clients(db_session)
    return contacts_clients
    """users = await get_management_users(db_session)
    users_dict_list = objects_many2many2dict_list(users, 'ManagementUsers')
    return users_dict_list"""