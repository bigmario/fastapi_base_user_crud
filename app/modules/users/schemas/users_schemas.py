from typing import Any, Optional

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    email: str
    name: str
    last_name: str
    phone: str


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[str] = None
    name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None

    class Config:
        exclude_unset = True


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
