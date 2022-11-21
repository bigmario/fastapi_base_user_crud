from typing import List, Optional
from fastapi import Body, BackgroundTasks, HTTPException
from fastapi import APIRouter, status, Depends

from sqlalchemy.orm import Session

from app.core.database.schemas import User, UserCreate
from app.core.database.services import get_db
from app.core.database.repositories import UserRepo


users_router = APIRouter(
    tags=["Users"],
)


@users_router.post("/users", response_model=User, status_code=201)
async def create_item(item_request: UserCreate, db: Session = Depends(get_db)):
    """
    Create an Item and store it in the database
    """

    db_item = UserRepo.fetch_by_name(db, name=item_request.name)
    if db_item:
        raise HTTPException(status_code=400, detail="Item already exists!")

    return await UserRepo.create(db=db, user=item_request)


@users_router.get("/users", response_model=List[User])
def get_all_items(name: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Get all the Items stored in database
    """
    if name:
        items = []
        db_item = UserRepo.fetch_by_name(db, name)
        items.append(db_item)
        return items
    else:
        return UserRepo.fetch_all(db)
