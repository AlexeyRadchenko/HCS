from datetime import timedelta
from re import I
from fastapi import APIRouter, Form
from fastapi import Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordRequestForm
from six import create_unbound_method
from sqlalchemy.ext.asyncio.session import AsyncSession
from typing import List

from ..settings.settings import settings
from ..security.token_model import Token
from ..security.user_model import User, UserInDB, ManagementUserInDB
from ..security.authentification_user import authenticate_user, create_access_token, get_password_hash
from ..security.user_data_depends import get_current_active_user
from ..database.database import get_async_session, objects_many2many2dict_list
from ..database.management_users.crud import create_management_user, update_management_user, get_management_users
from ..database.management_users.models import ManagementUsers
from ..database.management_users.schemas import ManagementUserSchema


router = APIRouter()

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db_session: AsyncSession = Depends(get_async_session)):
    print(form_data)
    user = await authenticate_user(db_session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorect username or password"
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.login, "scopes": user.scopes},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/management_users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.get("/management_users/users", response_model=List[ManagementUserInDB])
async def get_management_users_list(
    current_user: User = Security(get_current_active_user, scopes=[settings.ADMIN_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session)
    ):
    users = await get_management_users(db_session)
    users_dict_list = objects_many2many2dict_list(users, 'ManagementUsers')
    return users_dict_list

@router.post("/management_users/create_user")
async def create_management_user_handler(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db_session: AsyncSession = Depends(get_async_session), 
    current_user: User = Security(get_current_active_user, scopes=[settings.ADMIN_SCOPE])
):
    #print(form_data.username, form_data.password, form_data.scopes)
    hash_password = get_password_hash(form_data.password)
    user = ManagementUsers(
        login=form_data.username, hashed_password=hash_password, is_active=True, is_superuser=False
    )
    created_user_in_db = await create_management_user(db_session, user)
    user = ManagementUserSchema(created_user_in_db)
    return f"managment user --{user.login}-- is created"

@router.put("/management_users/update_user", response_model=User)
async def update_management_user_data_handler(
    user: UserInDB,
    db_session: AsyncSession = Depends(get_async_session),
    current_user: User = Security(get_current_active_user, scopes=[settings.ADMIN_SCOPE])
):  
    hash_password = get_password_hash(user.hashed_password)
    user.hashed_password = hash_password
    result = await update_management_user(db_session, user)
    return result