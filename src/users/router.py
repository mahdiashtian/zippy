from typing import List

from fastapi import APIRouter, Depends, Body
from fastapi import UploadFile
from sqlalchemy import Sequence, Row
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from src.annotations import _TP
from src.dependencies import get_db
from src.users import models
from src.users import schemas
from src.users import service
from src.users.dependencies import valid_user_create, valid_user_delete, valid_user_update, valid_user_get, \
    valid_user_follow
from src.utils import save_file

router = APIRouter()


@router.get("/", response_model=List[schemas.User], description="Get list users")
async def list_user(db: Annotated[Session, Depends(get_db)]) -> Sequence[Row[_TP]]:
    users = await service.get_users(db)
    return users


@router.get("/{user_id}/", response_model=schemas.User, description="Get detail user")
async def detail_user(valid_user_for_get: Annotated[models.User, Depends(valid_user_get)]) -> Row[_TP]:
    return valid_user_for_get


@router.post("/", response_model=schemas.User, description="Create new user")
async def create_user(user: Annotated[schemas.UserCreate, Depends(valid_user_create)],
                      db: Annotated[Session, Depends(get_db)]) -> Row[_TP]:
    return await service.create_user(user, db)


@router.delete("/{user_id}/", response_model=schemas.User, description="Delete user")
async def delete_user(valid_user_for_delete: Annotated[schemas.User, Depends(valid_user_delete)],
                      db: Annotated[Session, Depends(get_db)]) -> schemas.User:
    await service.delete_user(valid_user_for_delete, db)
    return valid_user_for_delete


@router.patch("/{user_id}/", response_model=schemas.User, description="Update user")
async def update_user(valid_user_for_update: Annotated[models.User, Depends(valid_user_update)],
                      data: Annotated[schemas.UserUpdate, Body()],
                      db: Annotated[Session, Depends(get_db)]) -> Row[_TP]:
    return await service.update_user(data, valid_user_for_update, db)


@router.patch("/{user_id}/change-image", response_model=schemas.User, description="Change user image")
async def change_image(valid_user_for_update: Annotated[models.User, Depends(valid_user_update)],
                       db: Annotated[Session, Depends(get_db)],
                       file: Annotated[UploadFile, bytes] = None) -> Row[_TP]:
    if file:
        path = await save_file(file)
    else:
        path = None
    return await service.change_image(path, valid_user_for_update, db)


@router.patch("/{user_id}/change-background-image", response_model=schemas.User,
              description="Change background user image")
async def change_background_image(valid_user_for_update: Annotated[models.User, Depends(valid_user_update)],
                                  db: Annotated[Session, Depends(get_db)],
                                  file: Annotated[UploadFile, bytes] = None) -> Row[_TP]:
    if file:
        path = await save_file(file)
    else:
        path = None
    return await service.change_background_image(path, valid_user_for_update, db)


@router.patch("/{user_id}/follow", response_model=schemas.User, description="Follow user")
async def follow_user(valid_user_for_update: Annotated[models.User, Depends(valid_user_update)],
                      valid_user_for_following: Annotated[models.User, Depends(valid_user_follow)],
                      db: Annotated[Session, Depends(get_db)]) -> Row[_TP]:
    return await service.follow_user(valid_user_for_update, valid_user_for_following, db)


@router.patch("/{user_id}/unfollow", response_model=schemas.User, description="Unfollow user")
async def unfollow_user(valid_user_for_update: Annotated[models.User, Depends(valid_user_update)],
                        valid_user_for_following: Annotated[models.User, Depends(valid_user_follow)],
                        db: Annotated[Session, Depends(get_db)]) -> Row[_TP]:
    return await service.unfollow_user(valid_user_for_update, valid_user_for_following, db)
