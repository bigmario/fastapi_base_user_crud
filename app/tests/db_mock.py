import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta
from jwt import encode

from app.app import app

from app.core.config import Settings

config = Settings()


def create_token(data: dict, expires_delta: timedelta | None = None) -> str:
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


SQLALCHEMY_DATABASE_URL = "sqlite:///./app/tests/test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

Base = declarative_base()


# Dependency
@pytest.fixture()
def get_db():
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_db():
    Base.metadata.create_all(bind=engine)


test_client = TestClient(app)
