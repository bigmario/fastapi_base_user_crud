from sqlalchemy.orm import Session
from fastapi import status, Depends
from fastapi.exceptions import HTTPException

from app.modules.users.schemas import UserCreate, UserUpdate
from app.modules.users.repositories import UserRepo


class UserService:
    def __init__(self, userRepo: UserRepo = Depends()):
        self.userRepo = userRepo

    async def create_user(self, item_request: UserCreate, db: Session):
        db_item = self.userRepo.fetch_by_email(db, email=item_request.email)
        if db_item:
            raise HTTPException(status_code=400, detail="User already exists!")

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

    async def get_user_by_id(self, user_id: int, db: Session):
        db_item = self.userRepo.fetch_by_id(db, user_id)
        if not db_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User Id not found!"
            )
        else:
            return db_item

    async def get_user_by_email(self, email: str, db: Session):
        db_item = self.userRepo.fetch_by_email(db, email)
        return db_item

    async def update_user(self, user_id: int, db: Session, item_request: UserUpdate):
        return self.userRepo.update(db, user_id, item_request)

    async def delete_user(self, user_id: int, db: Session):
        return self.userRepo.delete(db, user_id)
