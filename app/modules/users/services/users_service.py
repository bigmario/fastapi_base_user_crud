from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import status, Body, BackgroundTasks, HTTPException, Depends

from app.modules.users.repositories import UserRepo
from app.core.database.schemas import User, UserCreate


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
