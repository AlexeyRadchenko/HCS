from fastapi import APIRouter, Depends, Security
from sqlalchemy.ext.asyncio.session import AsyncSession

from ..database.accounts.schemas import AccountSchema
from ..database.database import get_async_session
from ..database.accounts.crud import get_account_data_by_account_num
from ..security.access_depends import user_scope_authorize
from ..settings.settings import settings

router = APIRouter()


@router.get("/account/{account}/data", response_model=AccountSchema)
async def create_contact_address_handler(
    account: str,
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.ACCOUNT_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session)
    ):
    account_data_in_db = await get_account_data_by_account_num(db_session, account)
    print('---------------------------------', account_data_in_db.account_params)
    return account_data_in_db