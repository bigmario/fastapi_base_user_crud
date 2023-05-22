from typing import Optional, Any

from pydantic import BaseModel, Field, EmailStr


class UserBase(BaseModel):
    email: EmailStr = Field(...)
    name: str = Field(...)
    last_name: str = Field(...)
    image: str = Field(...)


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

    class Config:
        schema_extra = {
            "example": {
                "email": "mail@mail.com",
                "name": "John",
                "last_name": "Doe",
                "image": "+58-000000000",
                "password": "12345678",
            }
        }


class UserUpdate(BaseModel):
    # email: Optional[EmailStr] = Field(default=None)
    name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)
    image: Optional[str] = Field(default=None)

    class Config:
        exclude_unset = True


class User(UserBase):
    id: int = Field(...)
    createdAt: str = Field(...)
    updatedAt: str = Field(...)
    deletedAt: Optional[str] = Field(...)

    class Config:
        orm_mode = True
