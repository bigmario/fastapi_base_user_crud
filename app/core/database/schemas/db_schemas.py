from typing import Any, Optional

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: str
    name: str
    last_name: str


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: str | None = None
    name: str | None = None
    last_name: str | None = None

    class Config:
        exclude_unset = True


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
