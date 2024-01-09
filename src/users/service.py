from typing import Union, Type

from fastapi import Path
from sqlalchemy import Row, Sequence
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from src.annotations import _TP
from src.users import models
from src.users import schemas


async def get_users(db: Session) -> Sequence[Row[_TP]]:
    result = db.query(models.User).order_by('id').all()
    return result


async def get_user_by_id(user_id: Annotated[int, Path(example=1)],
                         db: Session) -> Union[Type[models.User], None]:
    result = db.query(models.User).filter(
        models.User.id == user_id).first()
    if result:
        return result
    return None


async def get_user_by_username(username: Annotated[str, Path(example="username")],
                               db: Session) -> Union[Type[models.User], None]:
    result = db.query(models.User).filter(
        models.User.username == username).first()
    if result:
        return result
    return None


async def create_user(data: schemas.UserCreate,
                      db: Session) -> models.User:
    new_user = models.User(**dict(data))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_user(data: Union[schemas.UserUpdate, dict], user,
                      db: Session) -> models.User:
    if isinstance(data, dict):
        data_without_none = data
    else:
        data_without_none = data.dict(exclude_unset=True)
    for k, v in data_without_none.items():
        setattr(user, k, v)
    db.commit()
    db.refresh(user)
    return user


async def delete_user(user: models.User,
                      db: Session) -> models.User:
    db.delete(user)
    db.commit()
    return user


async def change_image(path: Union[str, None], user: models.User,
                       db: Session) -> models.User:
    data = dict(image=path)
    updated_user = await update_user(data, user, db)
    return updated_user


async def change_background_image(path: Union[str, None], user: models.User,
                                  db: Session) -> models.User:
    data = dict(background_image=path)
    updated_user = await update_user(data, user, db)
    return updated_user


async def follow_user(user: models.User, followed_user: models.User, db: Session) -> models.User:
    followed_users = user.followed_users
    followed_users.append(followed_user)
    data = dict(followed_users=followed_users)
    updated_user = await update_user(data, user, db)
    return updated_user


async def unfollow_user(user: models.User, followed_user: models.User, db: Session) -> models.User:
    followed_users = user.followed_users
    followed_users.remove(followed_user)
    data = dict(followed_users=followed_users)
    updated_user = await update_user(data, user, db)
    return updated_user
