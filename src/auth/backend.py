from fastapi import Depends
from starlette.authentication import AuthenticationBackend

from src.dependencies import get_current_user


class BearerTokenAuthBackend(AuthenticationBackend):
    async def authenticate(self, request, user: str = Depends(get_current_user)):
        return "", user
