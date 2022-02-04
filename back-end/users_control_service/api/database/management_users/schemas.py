from pydantic import BaseModel

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
