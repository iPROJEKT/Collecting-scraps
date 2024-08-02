from typing import Optional

from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    database_url: str
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
    spreadsheet_id: Optional[str] = None

    class Config:
        env_file = '.env'


settings = Settings()
