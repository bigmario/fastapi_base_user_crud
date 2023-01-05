from fastapi import Body, APIRouter, status, Depends, Query, Path
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app.core.database.services import get_db
from app.modules.auth.schemas import LoginResponse, RecoveryBody, ResetPasswordBody
from app.modules.auth.services import AuthService

auth_router = APIRouter(
    tags=["Auth"],
)


@auth_router.post(path="/auth/login", response_model=LoginResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(),
) -> LoginResponse:
    return await auth_service.login(form_data=form_data)


@auth_router.post(path="/auth/recovery")
async def send_password_recovery_mail(
    body: RecoveryBody, auth_service: AuthService = Depends()
):
    return await auth_service.send_recovery(body)


@auth_router.post(path="/auth/reset-password")
async def reset_password(
    body: ResetPasswordBody, auth_service: AuthService = Depends()
):
    return await auth_service.reset_password(body)
