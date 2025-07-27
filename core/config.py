from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_ID_ONE_SIGNAL : Optional[str] =None
    BASE_URL_ONE_SIGNAL:Optional[str] =None
    DATABASE_URL: Optional[str] =None
    APIKEY_DEV: Optional[str] =None
    ACCESS_TOKEN_EXPIRE_MINUTES:Optional[int] =None
    REFRESH_TOKEN_EXPIRE_DAYS:Optional[int] =None
    OBTENER_VERSION_MOVIL : Optional[str] =None

    class Config:
        env_file =".env"

settings = Settings()