from typing import Type

from fastapi import Depends, UploadFile
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from psql_database import SessionLocal
from src.config import settings
from src.exceptions import NotAuthenticated, BadRequest
from src.security import OAuth2PasswordBearerWS
from src.social.exceptions import NotAuthenticatedWS
from src.users import service, models

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/login")
oauth2_bearer_ws = OAuth2PasswordBearerWS(tokenUrl="/auth/login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)],
                           db: Annotated[Session, Depends(get_db)]) -> Type[models.User]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        user_id: int = payload.get("id", None)
    except jwt.JWTError:
        raise NotAuthenticated

    else:
        if user_id is None:
            raise NotAuthenticated
        user = await service.get_user_by_id(user_id, db)
        if user is None:
            raise NotAuthenticated
        return user


async def get_current_user_ws(token: Annotated[str, Depends(oauth2_bearer_ws)],
                              db: Annotated[Session, Depends(get_db)]) -> Type[models.User]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        user_id: int = payload.get("id", None)
    except jwt.JWTError:
        raise NotAuthenticatedWS

    else:
        if user_id is None:
            raise NotAuthenticatedWS
        user = await service.get_user_by_id(user_id, db)
        if user is None:
            raise NotAuthenticatedWS
        return user


async def valid_file(file: UploadFile) -> UploadFile:
    if file.content_type not in settings.MEDIA.ALLOWED_EXTENSIONS:
        raise BadRequest
    if file.size > settings.MEDIA.MAX_FILE_SIZE:
        raise BadRequest
    return file
