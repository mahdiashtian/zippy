from typing import Type

from fastapi import Depends
from fastapi import Path
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from src.dependencies import get_db
from src.social import models
from src.social import service
from src.social.exceptions import RoomNotFoundWS


async def valid_room_get(room_id: Annotated[int, Path()],
                         db: Annotated[Session, Depends(get_db)]) -> Type[models.Room]:
    room = await service.get_room(room_id, db)
    if not room:
        raise RoomNotFoundWS
    return room
