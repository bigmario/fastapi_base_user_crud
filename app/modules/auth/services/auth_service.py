import bcrypt

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException

from sqlalchemy.orm import Session
from app.core.config import Settings
from app.core.database.services import get_db
from app.core.libs import create_token

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
        user = await self.user_service.get_user_by_email(form_data.username, self.db)
        if not user:
            raise HTTPException(status_code=400, detail="Incorrect email or password")
        hashed_password = user.password

        if bcrypt.checkpw(form_password, hashed_password.encode("utf-8")):
            payload = {
                "sub": user.id,
                "email": user.email,
                "name": user.name,
                "last_name": user.last_name,
                "phone": user.phone,
            }
            return {
                "access_token": await create_token(payload),
                "token_type": "bearer",
            }
        else:
            raise HTTPException(
                status_code=400, detail="Incorrect username or password"
            )
