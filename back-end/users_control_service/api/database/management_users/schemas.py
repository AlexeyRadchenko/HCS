from pydantic import BaseModel
from typing import Optional

class ManagementUserBaseSchema(BaseModel):
    login: str

class ManagementUserCreateSchema(ManagementUserBaseSchema):
    password: str

class ManagementUserSchema(ManagementUserBaseSchema):
    id: int
    name: Optional[str]
    second_name: Optional[str]
    surname: Optional[str]
    hashed_password: str
    email: Optional[str]
    is_active: bool
    is_superuser: bool

    class Config:
        orm_mode = True