from fastapi import Body, BackgroundTasks
from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse

from ..schemas.post_email import Email

from ..service.email_service import EmailService


email_router = APIRouter(tags=["Contact"])


@email_router.post(
    path="/contact/async",
    status_code=status.HTTP_200_OK,
)
async def send_email_asynchronous(
    body: Email = Body(...),
    email_service: EmailService = Depends(),
):
    await email_service.send_email_async(body)
    return JSONResponse(
        {"Message": "Email Successfully Sent!!"}, status_code=status.HTTP_200_OK
    )


@email_router.post(
    path="/contact/bg-task",
    status_code=status.HTTP_200_OK,
)
def send_email_backgroundtasks(
    background_tasks: BackgroundTasks,
    body: Email = Body(...),
    email_service: EmailService = Depends(),
):
    email_service.send_email_background(background_tasks, body)
    return JSONResponse(
        {"Message": "Email Successfully Sent!!"}, status_code=status.HTTP_200_OK
    )
