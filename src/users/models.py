from datetime import datetime
from typing import List, Optional

from sqlalchemy import Integer, Enum, DateTime, String, Boolean, Column, ForeignKey, Table
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, column_property, validates, relationship

from src.fields import ImageField
from src.psql_database import Base
from src.users.constants import GenderChoices
from src.users.fields import Password

followers_association = Table(
    "followers_association",
    Base.metadata,
    Column("follower_id", Integer, ForeignKey("users.id")),
    Column("followed_id", Integer, ForeignKey("users.id")),

)


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    password: Mapped[str] = mapped_column(Password)
    created_at: Mapped[str] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[str] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    first_name: Mapped[str] = mapped_column(String, nullable=True)
    last_name: Mapped[str] = mapped_column(String, nullable=True)
    email: Mapped[str] = mapped_column(String, index=True, nullable=True)
    gender: Mapped[str] = mapped_column(Enum(GenderChoices), default=GenderChoices.DEFAULT)
    phone_number: Mapped[str] = mapped_column(String, index=True, nullable=True)
    image: Mapped[str] = mapped_column(ImageField, nullable=True)
    background_image: Mapped[str] = mapped_column(ImageField, nullable=True)
    biography: Mapped[str] = mapped_column(String, nullable=True)
    date_of_birth: Mapped[str] = mapped_column(DateTime, nullable=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    is_staff: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    followed_users: Mapped[List["User"]] = relationship(
        secondary=followers_association,
        primaryjoin=id == followers_association.c.follower_id,
        secondaryjoin=id == followers_association.c.followed_id,
        back_populates="followers",
        lazy="joined"
    )
    followers: Mapped[List["User"]] = relationship(
        secondary=followers_association,
        primaryjoin=id == followers_association.c.followed_id,
        secondaryjoin=id == followers_association.c.follower_id,
        back_populates="followed_users",
        lazy="joined"
    )
    room_id: Mapped[Optional[int]] = mapped_column(ForeignKey("rooms.id"))
    room: Mapped["Room"] = relationship(back_populates="users")

    full_name: Mapped[str] = column_property(first_name + " " + last_name)

    @validates('password')
    def _validate_password(self, key, password):
        return getattr(type(self), key).type.validator(password)
