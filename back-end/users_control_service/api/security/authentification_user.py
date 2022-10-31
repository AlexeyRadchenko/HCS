from datetime import datetime, timedelta
from typing import Optional

from passlib.context import CryptContext
from jose import jwt
from fastapi.security import OAuth2PasswordBearer

from .user_model import ManagementUserInDB, UserInDB, AccountUserInDB, AccountUser
from ..settings.settings import settings

from ..database.management_users.crud import get_management_user_by_login
from ..database.account_users.crud import get_account_user_by_a_s_h_a, get_account_user_by_account
from ..database.database import row2dict, user_many2many2dict, account_user_many2many2dict

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

async def get_account_user(db_session, account: str):
    user = await get_account_user_by_account(db_session, account)
    if not user:
        return None
    return AccountUser.from_orm(user)    


async def authenticate_management_user(db_session, login: str, password: str):
    user = await get_management_user_by_login(db_session, login)
    if not user:
        return False
    user_dict = user_many2many2dict(user)
    user_db = ManagementUserInDB(**user_dict)    
    if not verify_password(password, user_dict['hashed_password']):
        return False
    return user_db

async def authenticate_account_user(db_session, account: str, password: str, street: str, house: str, appartment: str):
    user = await get_account_user_by_a_s_h_a (db_session, account, street, house, appartment)
    if not user:
        return False
    user_db = AccountUserInDB.from_orm(user)
    if not verify_password(password, user.hashed_password):
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
