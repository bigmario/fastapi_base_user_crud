from pydantic import BaseSettings


class Settings(BaseSettings):
    mail_username: str
    mail_password: str
    mail_from: str
    mail_to: str
    mail_port: str
    mail_server: str
    mail_from_name: str

    class Config:
        env_file = ".env"
