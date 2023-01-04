from typing import Optional
from fastapi import Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.exceptions import HTTPException

from app.modules.auth.services import validate_token


class JWTGuard(HTTPBearer):
    async def __call__(
        self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        auth = await super().__call__(request)
        try:
            await validate_token(auth.credentials)
        except:
            raise HTTPException(status_code=403, detail="invalid credential")
