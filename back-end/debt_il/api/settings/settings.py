from yaml import safe_load, YAMLError
from pathlib import Path
from pydantic import BaseModel

"""Loading settings variable frome api.yaml

"""
PATH = Path(__file__).parent.resolve()
API_CONFIG_FILE = "api_config.yaml"

class Settings(BaseModel):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    CRYPT_CONTEXT_SCHEME: str
    PWD_CONTEXT_DEPRECATED: str
    TOKEN_URL: str
    DATABASE_URL: str
    SELF_USER_SCOPE: str
    ADMIN_SCOPE: str
    MANAGEMENT_DEBT_IL_SCOPE: str
    DEBT_IL_UPLOAD_PATH: str
    FILE_STORAGE_PATH: str
    JURIST_GROUP_SCOPE: str
    DEBT_IL_EGRN_UPLOAD_PATH: str
    DEBT_IL_ACCOUNTS_PASSPORT_UPLOAD_PATH: str

with open(f"{PATH}/{API_CONFIG_FILE}", "r") as stream:
    try:
        cfg_data = safe_load(stream)
        settings = Settings(**cfg_data)
        print('Contacts config----->', settings)
    except YAMLError as exc:
        print(exc)