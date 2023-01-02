import bcrypt
from datetime import datetime, timedelta
from jwt import encode, decode
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException

from sqlalchemy.orm import Session
from app.core.config import Settings
from app.core.database.services import get_db

from app.core.database.schemas import UserBase
from app.modules.users.services import UserService


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
config = Settings()


class AuthService:
    def __init__(
        self,
        user_service: UserService = Depends(),
        db: Session = Depends(get_db),
    ):
        self.user_service = user_service
        self.db = db

    async def login(
        self,
        form_data: OAuth2PasswordRequestForm,
    ):

        form_password = form_data.password.encode("utf-8")
        user = await self.user_service.get_user_by_username(form_data.username, self.db)
        if not user:
            raise HTTPException(
                status_code=400, detail="Incorrect username or password"
            )
        hashed_password = user.password

        if bcrypt.checkpw(form_password, hashed_password.encode("utf-8")):
            payload = {
                "sub": user.id,
                "name": user.name,
                "last_name": user.last_name,
                "email": user.email,
            }
            return {
                "access_token": await self.__create_token(payload),
                "token_type": "bearer",
            }
        else:
            raise HTTPException(
                status_code=400, detail="Incorrect username or password"
            )

    async def __create_token(
        self, data: dict, expires_delta: timedelta | None = None
    ) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_token: str = encode(
            payload=to_encode, key=config.jwt_secret, algorithm="HS256"
        )
        return encoded_token

    async def __validate_token(self, token: str) -> dict:
        veryfied_payload = decode(token, key=config.jwt_secret, algorithm=["HS256"])
        return veryfied_payload
