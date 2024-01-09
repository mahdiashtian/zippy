from datetime import datetime
from typing import Union, List

from pydantic import BaseModel
from pydantic import Field
from typing_extensions import Annotated

from src.users.constants import GenderChoices


class PasswordHashModel(BaseModel):
    hash: str


class UserCreate(BaseModel):
    username: Annotated[str, Field(pattern="^[a-zA-Z0-9_-]{3,30}$")]
    password: Annotated[
        Union[str, PasswordHashModel],
        Field(min_length=8, max_length=255)]


class UserUpdate(BaseModel):
    username: Annotated[
        Union[str, None],
        Field(pattern="^[a-zA-Z0-9_-]{3,30}$")] = None
    first_name: Annotated[
        Union[str, None],
        Field(min_length=1, max_length=255)] = None
    last_name: Annotated[
        Union[str, None],
        Field(min_length=1, max_length=255)] = None
    email: Annotated[
        Union[str, None],
        Field(min_length=1, max_length=255)] = None
    gender: Annotated[
        Union[GenderChoices, None],
        Field(default=GenderChoices.DEFAULT)] = None
    phone_number: Annotated[
        Union[str, None],
        Field(min_length=13, max_length=13)] = None
    biography: Annotated[
        Union[str, None],
        Field()] = None
    date_of_birth: Annotated[
        Union[datetime, None],
        Field()] = None


class UserRead(UserUpdate):
    id: int
    is_superuser: Annotated[bool, Field()]
    is_staff: Annotated[bool, Field()]
    is_active: Annotated[bool, Field()]
    created_at: Annotated[datetime, Field()]
    updated_at: Annotated[datetime, Field()]
    image: Annotated[Union[str, None], Field()] = None
    background_image: Annotated[Union[str, None], Field()] = None

    class Config:
        from_attributes = True


class User(UserRead):
    followed_users: Annotated[List["UserRead"], Field()] = []
    followers: Annotated[List["UserRead"], Field()] = []

    class Config:
        from_attributes = True
