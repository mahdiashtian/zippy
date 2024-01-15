from typing import Optional

from fastapi.security import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.websockets import WebSocket

from src.social.exceptions import NotAuthenticatedWS


class OAuth2PasswordBearerWS(OAuth2PasswordBearer):
    async def __call__(self, websocket: WebSocket) -> Optional[str]:
        authorization = websocket.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise NotAuthenticatedWS
            else:
                return None
        return param
