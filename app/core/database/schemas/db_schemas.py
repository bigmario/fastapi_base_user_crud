from typing import Any, Optional

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: str
    name: str
    last_name: str
    email: str


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    name: Optional[str] = None
    last_name: Optional[str] = None

    class Config:
        exclude_unset = True


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
