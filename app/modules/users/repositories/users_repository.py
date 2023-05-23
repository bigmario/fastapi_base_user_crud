import bcrypt
from typing import Any, List
from prisma import Prisma
from pydantic import parse_obj_as

from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

import app.modules.users.schemas.users_schemas as schemas


class UserRepo:
    def set_password(self, pw: str):
        pwhash = bcrypt.hashpw(pw.encode("utf8"), bcrypt.gensalt())
        password_hash = pwhash.decode(
            "utf8"
        )  # decode the hash to prevent is encoded twice
        return password_hash

    async def create(self, user: schemas.UserCreate):
        db = Prisma()
        await db.connect()
        user = await db.user.create(
            data={
                "name": user.name,
                "lastName": user.lastName,
                "image": user.image,
                "session": {
                    "create": {
                        "password": self.set_password(user.password),
                        "email": user.email,
                        "roleId": int(user.roleId),
                    },
                },
            },
            include={"session": True},
        )
        await db.disconnect()
        return user

    async def fetch_by_id(self, _id: int):
        db = Prisma()
        await db.connect()
        user = await db.user.find_unique(
            where={"id": int(_id)}, include={"session": True}
        )
        await db.disconnect()
        return user

    async def fetch_by_name(self, name: str):
        db = Prisma(auto_register=True)
        await db.connect()
        user = await db.user.find_first(where={"name": name}, include={"session": True})
        user.pop()
        await db.disconnect()
        return user

    async def fetch_by_email(self, email: str):
        db = Prisma(auto_register=True)
        await db.connect()
        user = await db.user.find_first(
            where={"session": {"is": {"email": {"equals": email}}}},
            include={"session": True},
        )
        await db.disconnect()
        return user

    async def fetch_all(self, skip: int = 0, limit: int = 100):
        db = Prisma(auto_register=True)
        await db.connect()
        users = await db.user.find_many(
            skip=skip,
            take=limit,
            include={"session": True},
        )
        await db.disconnect()
        return users

    async def delete(self, user_id: int):
        db = Prisma(auto_register=True)
        await db.connect()
        users = await db.user.delete(where={"id": user_id})
        await db.disconnect()
        return users

    async def update(self, user_id: int, user_data: schemas.UserUpdate):
        # db = Prisma(auto_register=True)
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
