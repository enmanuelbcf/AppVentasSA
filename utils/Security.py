import bcrypt
from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader

from app.constants.general import API_KEY_NAME
from core.config import settings


def hash_password(password: str) -> str:
    pwd = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd, salt)
    return hashed.decode('utf-8')


def verify_salt(password: str, hashed_password_from_db) -> bool:
    psd = password.encode('utf-8')

    if isinstance(hashed_password_from_db, str):
        hashed_bytes = hashed_password_from_db.encode('utf-8')
    elif isinstance(hashed_password_from_db, memoryview):
        hashed_bytes = bytes(hashed_password_from_db)
    else:
        hashed_bytes = hashed_password_from_db

    return bcrypt.checkpw(psd, hashed_bytes)


api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def verificar_apy_key(
        api_key: str = Depends(api_key_header)
):
    Api = settings.APIKEY_DEV
    if not api_key:
        raise HTTPException(status_code=403, detail="API Key requerida")

    if api_key != Api:
            raise HTTPException(status_code=403, detail="API Key inválida")

    return True