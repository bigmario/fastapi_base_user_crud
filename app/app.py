from fastapi import FastAPI, Depends, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

from app.core.auth.controllers import auth_router
from app.modules.users.controllers import users_router

from app.core.database import create_db


app = FastAPI()
app.title = "FastAPI Base User CRUD with Authentication"
app.description = """
    API developed with FastAPI for basic user administration and authentication
    Mario Castro <mariocastro.pva@gmail.com>"""

origins = [
    "*",
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(users_router)


@app.on_event("startup")
async def start_db(db: Session = Depends(create_db)):
    create_db()


@app.get(path="/", summary="Index", tags=["Index"], status_code=status.HTTP_200_OK)
async def index():
    return JSONResponse(
        {
            "Framework": "FastAPI",
            "Message": "Base Users CRUD !!",
        }
    )
