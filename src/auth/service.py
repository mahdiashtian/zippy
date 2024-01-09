from typing import Union

from src.users import service
from src.users import models


async def authenticate(username: str, password: str) -> Union[models.User, bool]:
    user = await service.get_user_by_username(username)
    if not user:
        return False
    if not user.password == password:
        return False
    return user
