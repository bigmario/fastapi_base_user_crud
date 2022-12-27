from typing import List
from fastapi import Body, APIRouter, status, Depends, Query, Path
from fastapi.exceptions import HTTPException

from sqlalchemy.orm import Session

from app.core.database.schemas import User, UserCreate, UserUpdate
from app.core.database.services import get_db
from app.modules.users.services import UserService


users_router = APIRouter(
    tags=["Users"],
)


@users_router.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_item(
    item_request: UserCreate = Body(...),
    db: Session = Depends(get_db),
    userService: UserService = Depends(),
):
    """
    Create an Item and store it in the database
    """
    try:
        return await userService.create_user(item_request, db)
    except Exception as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@users_router.get("/users", response_model=List[User], status_code=status.HTTP_200_OK)
async def get_all_items(
    name: str = Query(default=None),
    db: Session = Depends(get_db),
    userService: UserService = Depends(),
):
    """
    Get all the Items stored in database
    """
    try:
        return await userService.get_users(name, db)
    except Exception as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@users_router.patch(
    path="/users/{user_id}",
    response_model=User,
    response_model_exclude_unset=True,
    status_code=status.HTTP_200_OK,
)
async def update_item(
    user_id: int = Path(...),
    item_request: UserUpdate = Body(...),
    db: Session = Depends(get_db),
    userService: UserService = Depends(),
):
    """
    Updateate an item in the database
    """
    try:
        return await userService.update_user(user_id, db, item_request)
    except Exception as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@users_router.delete(
    "/users/{user_id}", response_model=User, status_code=status.HTTP_200_OK
)
async def delete_item(
    user_id: int = Path(...),
    db: Session = Depends(get_db),
    userService: UserService = Depends(),
):
    """
    Delete an item in the database
    """
    try:
        return await userService.delete_user(user_id, db)
    except Exception as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
