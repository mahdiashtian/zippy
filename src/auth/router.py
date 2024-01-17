from fastapi import Depends, APIRouter
from fastapi import Form
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from src.auth import service
from src.auth.exceptions import IncorrectUsernameOrPassword
from src.auth.jwt import create_access_token, create_refresh_token
from src.auth.responses import JWTResponse
from src.auth.utils import set_jwt_cookies, unset_jwt_cookies
from src.config import settings
from src.dependencies import get_current_user, get_db
from src.exceptions import NotAuthenticated
from src.social.service import get_or_create_room
from src.users import service as user_service, models

router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_MINUTES = settings.REFRESH_TOKEN_EXPIRE_MINUTES


@router.post("/login/")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                db: Annotated[Session, Depends(get_db)]):
    user = await service.authenticate(form_data.username, form_data.password, db)
    if not user:
        raise IncorrectUsernameOrPassword

    access_token = await create_access_token(
        username=user.username,
        user_id=user.id,
        expires_delta=settings.ACCESS_TOKEN_LIFETIME
    )
    refresh_token = await create_refresh_token(
        username=user.username,
        user_id=user.id,
        expires_delta=settings.REFRESH_TOKEN_LIFETIME
    )
    response = JWTResponse(access_token=access_token, refresh_token=refresh_token)
    await set_jwt_cookies(response, access_token, refresh_token)
    room = await get_or_create_room(db)
    data = dict(room_id=room.id)
    await user_service.update_user(data, user, db)
    return response


@router.post("/refresh/")
async def refresh(refresh_token: Annotated[str, Form()],
                  db: Annotated[Session, Depends(get_db)]):
    try:
        token = refresh_token
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=settings.ALGORITHM
        )
    except jwt.JWTError:
        raise NotAuthenticated
    else:
        user_id: int = payload.get("id", None)
        user = await user_service.get_user_by_id(user_id, db)
        if user is None:
            raise NotAuthenticated

        access_token = await create_access_token(
            username=user.username,
            user_id=user.id,
            expires_delta=settings.ACCESS_TOKEN_LIFETIME
        )

        refresh_token = await create_refresh_token(
            username=user.username,
            user_id=user.id,
            expires_delta=settings.REFRESH_TOKEN_LIFETIME
        )
        response = JWTResponse(access_token=access_token, refresh_token=refresh_token)

        await set_jwt_cookies(response, access_token, refresh_token)
        room = await get_or_create_room(db)
        data = dict(room_id=room.id)
        await user_service.update_user(data, user, db)
        return response


@router.post("/logout/")
async def logout(user: Annotated[models.User, Depends(get_current_user)],
                 db: Annotated[Session, Depends(get_db)]):
    response = JSONResponse(content={"status": "ok"})
    response.delete_cookie(key="refresh_token", path="/")
    response.delete_cookie(key="access_token", path="/")
    await unset_jwt_cookies(response)
    data = dict(room_id=None)
    await user_service.update_user(data, user, db)
    return response
