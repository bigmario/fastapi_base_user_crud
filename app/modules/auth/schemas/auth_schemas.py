from pydantic import BaseModel, Field, EmailStr


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = Field(default="bearer")


class RecoveryBody(BaseModel):
    email: EmailStr = Field(...)


class ResetPasswordBody(BaseModel):
    token: str = Field(...)
    new_password: str = Field(..., min_length=8)
