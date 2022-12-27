from typing import List, Optional, Any
from fastapi import APIRouter, status, Depends, Query

from sqlalchemy.orm import Session

from app.core.database.schemas import User, UserCreate
from app.core.database.services import get_db
from app.modules.users.services import UserService


users_router = APIRouter(
    tags=["Users"],
)


@users_router.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_item(
    item_request: UserCreate,
    db: Session = Depends(get_db),
    userService: UserService = Depends(),
):
    """
    Create an Item and store it in the database
    """

    return await userService.create_user(item_request, db)


@users_router.get("/users", response_model=List[User], status_code=status.HTTP_200_OK)
async def get_all_items(
    name: Optional[str] | None = Query(),
    db: Session = Depends(get_db),
    userService: UserService = Depends(),
):
    """
    Get all the Items stored in database
    """

    return await userService.get_users(name, db)
