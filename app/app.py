from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

from .modules.users.controllers import users_router

from .core.database import create_db, get_db


app = FastAPI()

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

app.include_router(users_router)


@app.on_event("startup")
async def start_db(db: Session = Depends(create_db)):
    create_db()


@app.get(path="/", summary="Index", tags=["Index"])
async def index():
    return JSONResponse(
        {
            "Framework": "FastAPI",
            "Message": "Base Users CRUD !!",
        }
    )
