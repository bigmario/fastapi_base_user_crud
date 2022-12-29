from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import status, Body, BackgroundTasks, Depends
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder

from app.modules.users.repositories import UserRepo
from app.core.database.schemas import User, UserCreate, UserUpdate


class UserService:
    def __init__(self, userRepo: UserRepo = Depends()):
        self.userRepo = userRepo

    async def create_user(self, item_request: UserCreate, db: Session):
        db_item = self.userRepo.fetch_by_name(db, name=item_request.name)
        if db_item:
            raise HTTPException(status_code=400, detail="Item already exists!")

        return await self.userRepo.create(db, item_request)

    async def get_users(self, name: str, db: Session):
        if name:
            items = []
            db_item = self.userRepo.fetch_by_name(db, name)
            if not db_item:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Item not found!"
                )
            items.append(db_item)
            return items
        else:
            return self.userRepo.fetch_all(db)

    async def get_user_by_username(self, username: str, db: Session):
        db_item = self.userRepo.fetch_by_username(db, username)
        if not db_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Username not found!"
            )
        return db_item

    async def update_user(self, user_id: int, db: Session, item_request: UserUpdate):
        return self.userRepo.update(db, user_id, item_request)

    async def delete_user(self, user_id: int, db: Session):
        return self.userRepo.delete(db, user_id)
