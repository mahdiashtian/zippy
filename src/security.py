from typing import Optional

from fastapi import status, WebSocketDisconnect
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.websockets import WebSocket


class OAuth2PasswordBearerWS(OAuth2PasswordBearer):
    async def __call__(self, websocket: WebSocket) -> Optional[str]:
        authorization = websocket.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise WebSocketDisconnect(code=status.WS_1008_POLICY_VIOLATION,
                                          reason="Not authenticated")
            else:
                return None
        return param
