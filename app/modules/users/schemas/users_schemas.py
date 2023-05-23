from typing import Optional, Any

from pydantic import BaseModel, Field, EmailStr


class Session(BaseModel):
    email: EmailStr = Field(...)


class UserBase(BaseModel):
    name: str = Field(...)
    lastName: str = Field(...)
    image: Optional[str] = Field(...)
    session: Optional[Session]


class UserCreate(UserBase):
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=8)
    roleId: int = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "name": "John",
                "last_name": "Doe",
                "image": "+58-000000000",
                "email": "mail@mail.com",
                "password": "12345678",
                "roleId": 1,
            }
        }


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = Field(default=None)
    name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)
    image: Optional[str] = Field(default=None)

    class Config:
        exclude_unset = True


class User(UserBase):
    id: int = Field(...)

    class Config:
        orm_mode = True
