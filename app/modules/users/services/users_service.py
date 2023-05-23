from typing import List
from fastapi import status, Depends
from fastapi.exceptions import HTTPException

from prisma.models import user

from app.modules.users.schemas import UserCreate, UserUpdate
from app.modules.users.repositories import UserRepo


class UserService:
    def __init__(self, userRepo: UserRepo = Depends()):
        self.userRepo = userRepo

    async def create_user(self, item_request: UserCreate):
        db_item = await self.userRepo.fetch_by_email(email=item_request.email)
        if db_item:
            raise HTTPException(status_code=400, detail="User already exists!")

        return await self.userRepo.create(item_request)

    async def get_users(self, name: str):
        if name:
            users = await self.userRepo.fetch_by_name(name)
            if not users:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Item not found!"
                )
            return users
        else:
            return await self.userRepo.fetch_all()

    async def get_user_by_id(self, user_id: int):
        db_item = await self.userRepo.fetch_by_id(user_id)
        if not db_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User Id not found!"
            )
        else:
            return db_item

    async def get_user_by_email(self, email: str):
        db_item = await self.userRepo.fetch_by_email(email)
        return db_item

    async def update_user(self, user_id: int, item_request: UserUpdate):
        return await self.userRepo.update(user_id, item_request)

    async def delete_user(self, user_id: int):
        return await self.userRepo.delete(user_id)
