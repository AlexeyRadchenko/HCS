from typing import List, Optional
from pydantic import BaseModel
from uuid import UUID

class ContactsClientSchema(BaseModel):
    uuid: Optional[UUID]
    name: Optional[str]
    second_name: Optional[str]
    surname: Optional[str]
    note: Optional[str]
    client_del: Optional[bool]

    class Config:
        orm_mode = True


class ContactsAddressSchema(BaseModel):
    id: Optional[int]
    street: str
    house_number: str
    entrance: str
    appartment: str

    class Config:
        orm_mode = True

class ContactsOrganisationsSchema(BaseModel):
    id: Optional[int]
    full_name: str
    short_name: str

    class Config:
        orm_mode = True

class ContactsPhonesSchema(BaseModel):
    id: Optional[int]
    home_phone: str
    work_phone: str
    mobile_phone: str

    class Config:
        orm_mode = True

class ContactsEmailsOrMsgers(BaseModel):
    id: Optional[int]
    email: Optional[str]

class ContactsClientFullDataSchema(ContactsClientSchema):
    phones: Optional[ContactsPhonesSchema]
    emails: Optional[ContactsEmailsOrMsgers]
    address: Optional[List[ContactsAddressSchema]]
    organisations: Optional[List[ContactsOrganisationsSchema]]

    class Config:
        orm_mode = True
