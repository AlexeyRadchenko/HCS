from email.headerregistry import Address
from typing import List, Optional, Any
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

class ContactsAddressesSchema(BaseModel):
    id: Optional[int]
    street: str
    house_number: str
    entrance: str
    appartment: str
    organisation_id: int

    class Config:
        orm_mode = True 

class ContactsClientsAddressesSchema(BaseModel):
    client_uuid: Optional[UUID]
    address_id: Optional[int]
    full_owner:bool
    part_owner:bool
    part_size: Optional[str]
    address_data: ContactsAddressesSchema
    class Config:
        orm_mode = True
        
      
class ContactsAddressesHouseStreetOrgIdScheme(BaseModel):
    street: str
    house_number: str
    organisation_id: int

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
    client_uuid: Optional[UUID]
    home_phone: str
    work_phone: str
    mobile_phone: str

    class Config:
        orm_mode = True

class ContactsEmailsOrMsgers(BaseModel):
    id: Optional[int]
    client_uuid: Optional[UUID]
    email: str

    class Config:
        orm_mode = True

class ContactsClientFullDataSchema(ContactsClientSchema):
    phones: Optional[List[ContactsPhonesSchema]]
    emails: Optional[List[ContactsEmailsOrMsgers]]
    addresses: Optional[List[ContactsClientsAddressesSchema]]
    organisations: Optional[List[ContactsOrganisationsSchema]]

    class Config:
        orm_mode = True
