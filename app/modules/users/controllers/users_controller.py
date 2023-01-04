from fastapi import Body, APIRouter, status, Depends, Query, Path
from fastapi.exceptions import HTTPException
from fastapi_pagination import Page, paginate

from sqlalchemy.orm import Session

from app.core.database.services import get_db
from app.core.middlewares import JWTGuard

from app.modules.auth.services import oauth2_scheme
from app.modules.users.schemas import User, UserCreate, UserUpdate
from app.modules.users.services import UserService

users_router = APIRouter(tags=["Users"])


@users_router.post(
    path="/users",
    response_model=User,
    response_model_exclude_unset=True,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(oauth2_scheme), Depends(JWTGuard())],
)
async def create_user(
    item_request: UserCreate = Body(...),
    db: Session = Depends(get_db),
    userService: UserService = Depends(),
):
    """
    Create an User and store it in the database
    """
    try:
        return await userService.create_user(item_request, db)
    except Exception as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@users_router.get(
    path="/users",
    response_model=Page[User],
    response_model_exclude_unset=True,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(JWTGuard())],
)
async def get_all_users(
    name: str = Query(default=None),
    db: Session = Depends(get_db),
    userService: UserService = Depends(),
):
    """
    Get all the Users stored in database
    """
    try:
        users = await userService.get_users(name, db)
        return paginate(users)
    except Exception as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@users_router.get(
    path="/users/{user_id}",
    response_model=User,
    response_model_exclude_unset=True,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(JWTGuard())],
)
async def get_user_by_id(
    user_id: str = Path(...),
    db: Session = Depends(get_db),
    userService: UserService = Depends(),
):
    """
    Get one User by Id
    """
    try:
        return await userService.get_user_by_id(user_id, db)
    except Exception as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@users_router.patch(
    path="/users/{user_id}",
    response_model=User,
    response_model_exclude_unset=True,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(JWTGuard())],
)
async def update_user(
    user_id: int = Path(...),
    item_request: UserUpdate = Body(...),
    db: Session = Depends(get_db),
    userService: UserService = Depends(),
):
    """
    Update an User in the database
    """
    try:
        return await userService.update_user(user_id, db, item_request)
    except Exception as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@users_router.delete(
    path="/users/{user_id}",
    response_model=User,
    response_model_exclude_unset=True,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(JWTGuard())],
)
async def delete_user(
    user_id: int = Path(...),
    db: Session = Depends(get_db),
    userService: UserService = Depends(),
):
    """
    Delete an User in the database
    """
    try:
        return await userService.delete_user(user_id, db)
    except Exception as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
