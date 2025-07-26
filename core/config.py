from typing import Optional
from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    APP_ID_ONE_SIGNAL: Optional[str] = None
    BASE_URL_ONE_SIGNAL: Optional[str] = None
    DATABASES_APP_VENTAS: Optional[str] = None
    APIKEY_DEV: Optional[str] = None

    class Config:
        env_file = ".env" if not os.getenv("RAILWAY_ENVIRONMENT") else None  # solo carga .env si no está en Railway

settings = Settings()
