from datetime import datetime
from typing import List

from sqlalchemy import Integer, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.psql_database import Base


class Room(Base):
    __tablename__ = 'rooms'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[str] = mapped_column(DateTime, default=datetime.utcnow)
    users: Mapped[List["User"]] = relationship("User", back_populates="room")
