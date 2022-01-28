from typing import List, Optional
from pydantic import BaseModel

from api.database.management_users.models import Base


class ManagementUserBaseSchema(BaseModel):
    login: str

class ManagementUserCreateSchema(ManagementUserBaseSchema):
    password: str

class ManagementUserSchema(ManagementUserBaseSchema):
    id: int
    is_active: bool
    is_superuser: bool

    class Config:
        orm_mode = True
