from typing import Optional, List
from pydantic import BaseModel
from yaml import StreamEndToken

class User(BaseModel):
    login: str
    name: Optional[str] = None
    second_name: Optional[str] = None
    surname: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None

class AccountUser(BaseModel):
    account: str
    name: Optional[str] = None
    second_name: Optional[str] = None
    surname: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None
    street: str
    house: str
    appartment: str

    class Config:
        orm_mode = True   

class UserInDB(User):
    id: int
    hashed_password: Optional[str] = None

    class Config:
        orm_mode = True

class ManagementUserInDB(User):
    id: int
    scopes: List[str] = None

    class Config:
        orm_mode = True
class AccountScopes(BaseModel):
    id: int
    scope_name: str
    active_scope: bool

    class Config:
        orm_mode = True

class AccountUserInDB(AccountUser):
    id: int
    account_scopes: Optional[List[AccountScopes]] = None
    hashed_password: Optional[str] = None

    class Config:
        orm_mode = True