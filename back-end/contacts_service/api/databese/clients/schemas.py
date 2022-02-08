from typing import List, Optional
from pydantic import BaseModel, Field
from uuid import uuid4, UUID

class ContactsClientSchema(BaseModel):
    uuid: UUID = Field(default_factory=uuid4)
    name: str
    second_name:str
    surname: str

class ContactsAddressSchema(BaseModel):
    street: str
    house_number: str
    entrance: str
    appartment: str

    class Config:
        orm_mode = True

class ContactsOrganisationsSchema(BaseModel):
    full_name: str
    short_name: str

    class Config:
        orm_mode = True

class ContactsCientFullDataSchema(ContactsClientSchema):
    addresses: List[ContactsAddressSchema]
    full_owner: bool
    part_owner:bool
    part_size: str
    organisations: List[ContactsOrganisationsSchema]

    class Config:
        orm_mode = True
