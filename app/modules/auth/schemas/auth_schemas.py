from pydantic import BaseModel, Field, EmailStr


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = Field(default="bearer")
