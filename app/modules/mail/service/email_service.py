import os
from fastapi import Body, status, BackgroundTasks

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

from app.modules.mail.config import config as conf
from app.modules.mail.schemas.post_email import Email


settings = conf.Settings()


class EmailService:
    def __init__(self):
        self.conf = ConnectionConfig(
            MAIL_USERNAME=settings.mail_username,
            MAIL_PASSWORD=settings.mail_password,
            MAIL_FROM=settings.mail_from,
            MAIL_PORT=settings.mail_port,
            MAIL_SERVER=settings.mail_server,
            MAIL_FROM_NAME=settings.mail_from_name,
            MAIL_STARTTLS=bool(settings.mail_use_tls),
            MAIL_SSL_TLS=bool(settings.mail_use_ssl),
            USE_CREDENTIALS=True,
            TEMPLATE_FOLDER=f"{os.getcwd()}/app/modules/mail/templates",
        )

    async def send_email_async(self, body: Email):

        message = MessageSchema(
            subject=body.subject,
            recipients=[settings.mail_to],
            template_body=body.body,
            subtype="html",
        )
        fm = FastMail(self.conf)
        await fm.send_message(message, template_name="email.html")

    def send_email_background(self, background_tasks: BackgroundTasks, body: Email):
        message = MessageSchema(
            subject=body.subject,
            recipients=[settings.mail_to],
            template_body=body.body,
            subtype="html",
        )

        fm = FastMail(self.conf)

        background_tasks.add_task(fm.send_message, message, template_name="email.html")
