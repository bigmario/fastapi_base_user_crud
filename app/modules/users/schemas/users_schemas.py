from typing import Any, Optional

from pydantic import BaseModel, Field, EmailStr


class UserBase(BaseModel):
    email: EmailStr = Field(...)
    name: str = Field(...)
    last_name: str = Field(...)
    phone: str = Field(...)


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

    class Config:
        schema_extra = {
            "example": {
                "email": "mail@mail.com",
                "name": "John",
                "last_name": "Doe",
                "phone": "+58-000000000",
                "password": "12345678",
            }
        }


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = Field(default=None)
    name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)
    phone: Optional[str] = Field(default=None)
    recovery_token: Optional[str] = Field(default=None)
    password: Optional[str] = Field(default=None)

    class Config:
        exclude_unset = True


class User(UserBase):
    id: int = Field(...)

    class Config:
        orm_mode = True
