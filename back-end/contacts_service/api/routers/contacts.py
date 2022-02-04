import imp
from fastapi import APIRouter, Depends
from fastapi import Security

from sqlalchemy.ext.asyncio.session import AsyncSession
from ..security.access_depends import user_scope_authorize
from ..settings.settings import settings
from ..databese.database import get_async_session
from ..databese.clients.schemas import ContactsCientFullDataSchema
from ..databese.clients.crud import get_contacts_clients

router = APIRouter()

"""@router.post("/management_users/create_user")
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
    """

@router.get("/contacts_users/users", response_model=ContactsCientFullDataSchema)
async def get_contacts_users_list(
    #user_auth: bool = Security(user_scope_authorize, scopes=[settings.MANAGEMENT_SCOPE])
    user_auth: bool = Security(user_scope_authorize, scopes=[settings.SELF_USER_SCOPE, settings.MANAGEMENT_CONTACTS_SCOPE]),
    db_session: AsyncSession = Depends(get_async_session)
    ):
    contacts_clients = get_contacts_clients(db_session)
    return contacts_clients
    """users = await get_management_users(db_session)
    users_dict_list = objects_many2many2dict_list(users, 'ManagementUsers')
    return users_dict_list"""