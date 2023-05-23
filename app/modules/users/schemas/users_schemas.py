from typing import Optional, Any

from pydantic import BaseModel, Field, EmailStr


class UserSession(BaseModel):
    email: Optional[EmailStr] = Field(default=None)
    recoveryToken: Optional[str] = Field(default=None, exclude=True)
    roleId: Optional[int] = Field(default=None)


class UserBase(BaseModel):
    name: str = Field(...)
    lastName: str = Field(...)
    image: Optional[str] = Field(default=None)
    session: Optional[UserSession] = Field(default=None)

    class Config:
        exclude_unset = True


class UserCreate(UserBase):
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=8, exclude=True)
    roleId: int = Field(...)

    class Config:
        exclude_unset = True
        schema_extra = {
            "example": {
                "name": "John",
                "lastName": "Doe",
                "image": "+58-000000000",
                "email": "mail@mail.com",
                "password": "12345678",
                "roleId": 1,
            }
        }


class UserUpdate(BaseModel):
    name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)
    image: Optional[str] = Field(default=None)
    email: Optional[EmailStr] = Field(default=None)
    recoveryToken: Optional[str] = Field(default=None)
    roleId: Optional[int] = Field(default=None)

    class Config:
        exclude_unset = True
        exclude_none = True


class User(UserBase):
    id: int = Field(...)

    class Config:
        exclude_unset = True
        orm_mode = True
