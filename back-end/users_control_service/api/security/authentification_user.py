from datetime import datetime, timedelta
from typing import Optional

from passlib.context import CryptContext
from jose import jwt
from fastapi.security import OAuth2PasswordBearer

from .user_model import ManagementUserInDB, UserInDB
from ..settings.settings import settings

from ..database.management_users.crud import get_management_user_by_login
from ..database.database import row2dict, user_many2many2dict

pwd_context = CryptContext(schemes=[settings.CRYPT_CONTEXT_SCHEME], deprecated=settings.PWD_CONTEXT_DEPRECATED)
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=settings.TOKEN_URL,
    scopes={}
)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def get_user(db_session, login: str):
    user = await get_management_user_by_login(db_session, login)
    if not user:
        return False
    user_dict = user_many2many2dict(user)
    return UserInDB(**user_dict)


async def authenticate_user(db_session, login: str, password: str):
    user = await get_management_user_by_login(db_session, login)
    if not user:
        return False
    user_dict = user_many2many2dict(user)
    user_db = ManagementUserInDB(**user_dict)    
    if not verify_password(password, user_dict['hashed_password']):
        return False
    return user_db

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
