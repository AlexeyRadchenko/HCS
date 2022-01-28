from api.security.authentification_user import get_password_hash
from api.database.management_users.crud import create_superuser
from api.database.database import async_session


async def init_superuser(login, password):
    db_session = async_session()
    print (db_session)
    hashed_password = get_password_hash(password)
    su = await create_superuser(db_session, login, hashed_password)
    await db_session.close()
    login = su.login
    print(f"Superuser {login} is created")
    