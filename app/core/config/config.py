import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    host: str
    port: int
    log_level: str
    reload: int
    db_name: str
    db_user: str
    db_password: str
    db_host: str
    db_port: int
    jwt_secret: str
    admin_password: str

    class Config:
        env_file = ".env"
