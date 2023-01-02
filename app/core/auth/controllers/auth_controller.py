from fastapi import Body, APIRouter, status, Depends, Query, Path
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session
from app.core.database.services import get_db
from app.core.auth.services import AuthService

auth_router = APIRouter(
    tags=["Auth"],
)


@auth_router.post("/auth/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(),
):
    return await auth_service.login(form_data=form_data)
