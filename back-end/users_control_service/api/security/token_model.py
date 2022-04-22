from typing import Optional, List
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    login: str
    username: Optional[str] = None
    scopes: List[str] = []

class AccountToken(BaseModel):
    access_token: str
    token_type: str

class AccountTokenData(BaseModel):
    account: str
    username: Optional[str] = None
    scopes: List[str] = []    