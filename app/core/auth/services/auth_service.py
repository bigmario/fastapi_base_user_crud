import bcrypt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException

from sqlalchemy.orm import Session
from app.core.database.services import get_db

from app.core.database.schemas import UserBase
from app.modules.users.services import UserService


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


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
        db: Session,
        form_data: OAuth2PasswordRequestForm,
    ):

        form_password = form_data.password.encode("utf-8")
        user = await self.user_service.get_user_by_username(form_data.username, db)
        if not user:
            raise HTTPException(
                status_code=400, detail="Incorrect username or password"
            )
        hashed_password = user.password

        if bcrypt.checkpw(
            form_data.password.encode("utf-8"), hashed_password.encode("utf-8")
        ):
            return {"access_token": user.username, "token_type": "bearer"}
        else:
            raise HTTPException(
                status_code=400, detail="Incorrect username or password"
            )
