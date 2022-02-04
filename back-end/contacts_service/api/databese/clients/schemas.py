from typing import List, Optional
from pydantic import BaseModel, Field
from uuid import uuid4, UUID

class ContactsClientSchema(BaseModel):
    uuid: UUID = Field(default_factory=uuid4)
    name: str
    second_name:str
    surname: str

class ContactsAddress(BaseModel):
    street: str
    house_number: str
    entrance: str
    appartment: str

class ContactsCientFullDataSchema(ContactsClientSchema):
    addresses: List[ContactsAddress]
    full_owner: bool
    part_owner:bool
    part_size: str

    class Config:
        orm_mode = True
