import bcrypt
from typing import Any, List
from prisma import Prisma
from pydantic import parse_obj_as

from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

import app.modules.users.schemas.users_schemas as schemas


class UserRepo:
    async def create(self, user: schemas.UserCreate):
        pass

    async def fetch_by_id(self, _id):
        db = Prisma()
        await db.connect()
        user = await db.user.find_unique(
            where={"id": _id},
        )
        await db.disconnect()
        return user

    async def fetch_by_name(self, name):
        db = Prisma()
        await db.connect()
        user = await db.user.find_first(
            where={"name": name}, include={"session": {"include": {"role": True}}}
        )
        await db.disconnect()
        return user

    async def fetch_by_email(self, email):
        db = Prisma()
        await db.connect()
        user = await db.session.find_first(
            where={"email": email}, include={"user": True, "role": True}
        )
        await db.disconnect()
        return user

    async def fetch_all(self, skip: int = 0, limit: int = 100):
        db = Prisma()
        await db.connect()
        users = await db.user.find_many(skip=skip, take=limit)
        await db.disconnect()
        return users

    async def delete(self, user_id):
        db = Prisma()
        await db.connect()
        users = await db.user.delete(user_id)
        await db.disconnect()
        return users

    async def update(self, user_id: int, user_data: schemas.UserUpdate):
        # db = Prisma()
        # await db.connect()
        return user_data
        # user = await db.user.update(
        #     where={
        #         'id': user_id
        #     },
        #     data={

        #     }
        # )
        # await db.disconnect()
        # return user
