from datetime import datetime, timedelta
from jwt import encode, decode

from app.core.config import Settings

config = Settings()


async def create_token(data: dict, expires_delta: timedelta | None = None) -> str:
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


async def validate_token(token: str) -> dict:
    veryfied_payload = decode(token, key=config.jwt_secret, algorithms=["HS256"])
    return veryfied_payload
