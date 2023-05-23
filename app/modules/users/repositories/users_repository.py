import bcrypt
from typing import Optional
from prisma import Prisma
from prisma.models import user

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
        newUser = await db.user.create(
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
        return newUser

    async def upsert(self, user: schemas.UserCreate, user_id: Optional[int] = None):
        db = Prisma()
        await db.connect()
        newUser = await db.user.upsert(
            where={"id": user_id},
            data={
                "create": {
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
                "update": {
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
            },
            include={"session": True},
        )
        await db.disconnect()
        return newUser

    async def fetch_by_id(self, _id: int):
        db = Prisma()
        await db.connect()
        user = await db.user.find_unique(
            where={"id": int(_id)}, include={"session": True}
        )
        await db.disconnect()
        return user

    async def fetch_by_name(self, name: str):
        db = Prisma()
        await db.connect()
        user = await db.user.find_many(
            where={"name": {"contains": name}}, include={"session": True}
        )
        await db.disconnect()
        return user

    async def fetch_by_email(self, email: str):
        db = Prisma()
        await db.connect()
        user = await db.user.find_first(
            include={"session": True},
            where={"session": {"is": {"email": {"equals": email}}}},
        )
        await db.disconnect()
        return user

    async def fetch_all(self, skip: int = 0, limit: int = 100):
        db = Prisma()
        await db.connect()
        users = await db.user.find_many(
            skip=skip,
            take=limit,
            include={"session": True},
        )
        await db.disconnect()
        return users

    async def delete(self, user_id: int):
        db = Prisma()
        await db.connect()
        users = await db.user.delete(where={"id": user_id})
        await db.disconnect()
        return users

    async def update(self, user_id: int, user_data: schemas.UserUpdate):
        db = Prisma()
        await db.connect()
        try:
            await db.user.update(
                where={"id": user_id},
                data={
                    "name": user_data.name if user_data.name else None,
                    "lastName": user_data.last_name if user_data.last_name else None,
                    "image": user_data.image if user_data.image else None,
                },
            )
        except:
            pass

        try:
            await db.session.update(
                where={user_id: user_id},
                data={
                    "email": user_data.email,
                    "recoveryToken": user_data.recoveryToken,
                    "role": {"connect": {"id": user_data.roleId}},
                },
            )
        except:
            pass

        await db.disconnect()
        return True
