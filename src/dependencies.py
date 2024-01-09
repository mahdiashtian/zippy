from fastapi import Depends, UploadFile
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from sqlalchemy import Row

from src.annotations import _TP
from src.config import settings
from src.exceptions import NotAuthenticated, BadRequest
from src.users import service
from psql_database import SessionLocal

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(token: str = Depends(oauth2_bearer)) -> Row[_TP]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        user_id: int = payload.get("id", None)
    except jwt.JWTError:
        raise NotAuthenticated
    else:
        if user_id is None:
            raise NotAuthenticated
        user = await service.get_user_by_id(user_id)
        if user is None:
            raise NotAuthenticated
        return user


async def valid_file(file: UploadFile) -> UploadFile:
    if file.content_type not in settings.MEDIA.ALLOWED_EXTENSIONS:
        raise BadRequest
    if file.size > settings.MEDIA.MAX_FILE_SIZE:
        raise BadRequest
    return file
