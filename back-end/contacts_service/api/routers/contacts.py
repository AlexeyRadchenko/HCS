import imp
from fastapi import APIRouter
from fastapi import Security

from ..security.access_depends import user_scope_authorize
from ..settings.settings import settings

router = APIRouter()

@router.get("/contacts_users/users")
async def get_contacts_users_list(
    #user_auth: bool = Security(user_scope_authorize, scopes=[settings.MANAGEMENT_SCOPE])
    user_auth: bool = Security(user_scope_authorize, scopes=["me"])
    #db_session: AsyncSession = Depends(get_async_session)
    ):
    return "access to Contacts grunted"
    """users = await get_management_users(db_session)
    users_dict_list = objects_many2many2dict_list(users, 'ManagementUsers')
    return users_dict_list"""