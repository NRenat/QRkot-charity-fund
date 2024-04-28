import os
from typing import Optional

from pydantic import BaseSettings, EmailStr
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    app_title: str = 'QRKot'
    app_description: str = 'Cat Charity Fund'
    secret: str = os.getenv('SECRET_KEY', 'SECRET_KEY')
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None
    database_url: str = os.getenv('DATABASE_URL',
                                  'sqlite+aiosqlite:///./fastapi.db')

    MIN_PASSWORD_LENGTH: int = 8

    type: Optional[str] = None
    project_id: Optional[str] = None
    private_key_id: Optional[str] = None
    private_key: Optional[str] = None
    client_email: Optional[str] = None
    client_id: Optional[str] = None
    auth_uri: Optional[str] = None
    token_uri: Optional[str] = None
    auth_provider_x509_cert_url: Optional[str] = None
    client_x509_cert_url: Optional[str] = None
    email: Optional[str] = None
    universe_domain: Optional[str] = None

    class Config:
        env_file = '../../.env'


settings = Settings()
