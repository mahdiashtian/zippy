from typing import Union, Type

from sqlalchemy.orm import Session

from src.users import service
from src.users import models


async def authenticate(username: str, password: str, db: Session) -> Union[Type[models.User], bool]:
    user = await service.get_user_by_username(username, db)
    if not user:
        return False
    if not user.password == password:
        return False
    return user
