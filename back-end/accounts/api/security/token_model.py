from pydantic import BaseModel
from typing import List, Optional

class TokenData(BaseModel):
    username: Optional[str] = None
    scopes: List[str] = []

class AccountToken(BaseModel):
    access_token: str
    token_type: str

class AccountTokenData(BaseModel):
    account: str
    username: Optional[str] = None
    scopes: List[str] = []