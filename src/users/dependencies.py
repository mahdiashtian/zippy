from typing import Type

from fastapi import Form, Path, Depends
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from src.dependencies import get_db
from src.users import service, models
from src.users.exceptions import UserAlreadyExists, UserDoesNotExist
from src.users.schemas import UserCreate


async def valid_user_create(username: Annotated[str, Form()],
                            password: Annotated[str, Form()],
                            db: Annotated[Session, Depends(get_db)]) -> UserCreate:
    if await service.get_user_by_username(username, db):
        raise UserAlreadyExists()
    user = UserCreate(username=username, password=password)
    return user


async def valid_user_follow(username: Annotated[str, Form()],
                            db: Annotated[Session, Depends(get_db)]) -> Type[models.User]:
    user = await service.get_user_by_username(username, db)
    if not user:
        raise UserDoesNotExist()
    return user


async def valid_user_base(user_id: Annotated[int, Path(example=1, description="id of user to get detail")],
                          db: Annotated[Session, Depends(get_db)]) -> Type[models.User]:
    user = await service.get_user_by_id(user_id, db)
    if not user:
        raise UserDoesNotExist()
    return user


async def valid_user_delete(valid_user: Annotated[Type[models.User], Depends(valid_user_base)]) -> Type[models.User]:
    return valid_user


async def valid_user_update(valid_user: Annotated[Type[models.User], Depends(valid_user_base)]) -> Type[models.User]:
    return valid_user


async def valid_user_get(valid_user: Annotated[Type[models.User], Depends(valid_user_base)]) -> Type[models.User]:
    return valid_user
