from typing import Optional, List
from pydantic import BaseModel

class User(BaseModel):
    login: str
    name: Optional[str] = None
    second_name: Optional[str] = None
    surname: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None


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