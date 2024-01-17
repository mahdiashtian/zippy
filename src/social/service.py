from typing import Union, Type

from sqlalchemy import func
from sqlalchemy.orm import Session

from src.social import models
from src.social.models import Room
from src.users.models import User


async def get_or_create_room(db: Session) -> Union[Type[models.Room], models.Room]:
    result = db.query(Room).join(User).group_by(Room.id).having(func.count(User.id) < 50).filter(
        Room.is_active == True
    ).first()
    if result:
        return result
    new_room: models.Room = models.Room()
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return new_room
