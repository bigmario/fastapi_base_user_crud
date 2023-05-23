import bcrypt
from prisma import Prisma

from fastapi import Depends, status, BackgroundTasks
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from app.core.config import Settings
from app.core.libs import create_token, validate_token

from app.modules.users.schemas import UserUpdate
from app.modules.auth.schemas import RecoveryBody, ResetPasswordBody
from app.modules.mail.schemas import Email, MailBody
from app.modules.users.services import UserService
from app.modules.mail.service import EmailService


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
config = Settings()


class AuthService:
    def __init__(
        self,
        background_tasks: BackgroundTasks,
        user_service: UserService = Depends(),
        mail_service: EmailService = Depends(),
    ):
        self.background_tasks = background_tasks
        self.user_service = user_service
        self.mail_service = mail_service

    async def login(
        self,
        form_data: OAuth2PasswordRequestForm,
    ):
        form_password = form_data.password.encode("utf-8")
        user = await self.user_service.get_user_by_email(form_data.username)
        if not user:
            raise HTTPException(status_code=400, detail="Incorrect email or password")
        hashed_password = user.session.password

        if bcrypt.checkpw(form_password, hashed_password.encode("utf-8")):
            payload = {
                "sub": user.id,
                "email": user.session.email,
                "name": user.name,
                "last_name": user.lastName,
            }
            return {
                "access_token": await create_token(payload),
                "token_type": "bearer",
            }
        else:
            raise HTTPException(
                status_code=400, detail="Incorrect username or password"
            )

    async def send_recovery(self, body: RecoveryBody):
        user = await self.user_service.get_user_by_email(body.email)
        if not user:
            raise HTTPException(status_code=404, detail="Not Found")

        payload = {"sub": user.user.id}
        recovery_token = await create_token(payload)
        link = f"http://myfrontend.com/recovery?token={recovery_token}"

        await self.user_service.update_user(
            user.id, UserUpdate(recovery_token=recovery_token)
        )

        body = Email(
            subject="Recovery Mail",
            body=MailBody(
                name="Admin",
                number="11111",
                message=f"Ingresa a este link => {link}",
                mail="admin@mail.com",
            ),
        )

        self.mail_service.send_email_background(self.background_tasks, body)

        return JSONResponse(
            {"Message": "Email Successfully Sent!!"}, status_code=status.HTTP_200_OK
        )

    async def reset_password(self, body: ResetPasswordBody):
        try:
            payload = await validate_token(body.token)
            user = await self.user_service.get_user_by_id(
                payload["sub"],
            )
            if user.recovery_token != body.token:
                raise HTTPException(status_code=401, detail="Unauthorized")

            salt = bcrypt.gensalt()
            hash = bcrypt.hashpw(body.new_password.encode("utf-8"), salt)

            await self.user_service.update_user(
                user.id, UserUpdate(password=hash, recovery_token=None)
            )

            return JSONResponse(
                {"Message": "Password Changed!!"}, status_code=status.HTTP_200_OK
            )
        except:
            raise HTTPException(status_code=400, detail="Unauthorized")
