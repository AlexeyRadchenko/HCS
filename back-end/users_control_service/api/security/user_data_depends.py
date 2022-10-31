from re import DEBUG
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlalchemy.ext.asyncio.session import AsyncSession

from .authentification_user import oauth2_scheme
from ..settings.settings import settings
from .token_model import TokenData
from .user_model import User
from .authentification_user import get_user, get_account_user
from ..database.database import get_async_session


from fastapi import Depends, HTTPException, status, Security
from fastapi.security import SecurityScopes

async def get_current_user(
    security_scopes: SecurityScopes,
    token: str = Depends(oauth2_scheme),
    db_session: AsyncSession = Depends(get_async_session)):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = f"Bearer"
    credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": authenticate_value},
        )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        login: str = payload.get("sub")
        if login is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, login=login)
    except (JWTError, ValidationError):
        raise credentials_exception
    user = await get_account_user(db_session, account=token_data.login)
    if user is None:
        user = await get_user(db_session, login=token_data.login)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user


async def get_current_active_user(current_user: User = Security(get_current_user, scopes=[settings.SELF_USER_SCOPE])):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user    