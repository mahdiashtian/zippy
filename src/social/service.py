from typing import Union, Type

from sqlalchemy.orm import Session

from src.social import models


async def get_room(room_id: int, db: Session) -> Type[models.Room]:
    return db.query(models.Room).filter(models.Room.id == room_id).first()


async def get_or_create_room(db: Session) -> Union[Type[models.Room], models.Room]:
    result = db.query(models.Room).filter(
        models.Room.is_active == True
    ).first()
    if result:
        return result
    new_room: models.Room = models.Room()
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return new_room
