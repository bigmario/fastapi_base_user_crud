import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from jwt import encode

from app.core.database.services.db_service import Base

from app.app import app
from app.core.database import get_db

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
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
        
app.dependency_overrides[get_db] = override_get_db

test_client = TestClient(app)