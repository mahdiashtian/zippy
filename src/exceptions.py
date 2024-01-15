from typing import Any, Dict

from fastapi import HTTPException, status, WebSocketException


class DetailedHTTPException(HTTPException):
    STATUS_CODE = status.HTTP_500_INTERNAL_SERVER_ERROR
    DETAIL = "Server error"

    def __init__(self, **kwargs: Dict[str, Any]) -> None:
        super().__init__(status_code=self.STATUS_CODE, detail=self.DETAIL, **kwargs)


class DetailedWSException(WebSocketException):
    STATUS_CODE = status.WS_1008_POLICY_VIOLATION
    DETAIL = "WebSocket error"

    def __init__(self) -> None:
        super().__init__(code=self.STATUS_CODE, reason=self.DETAIL)


class PermissionDenied(DetailedHTTPException):
    STATUS_CODE = status.HTTP_403_FORBIDDEN
    DETAIL = "Permission denied"


class NotFound(DetailedHTTPException):
    STATUS_CODE = status.HTTP_404_NOT_FOUND


class BadRequest(DetailedHTTPException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = "Bad Request"


class NotAuthenticated(DetailedHTTPException):
    STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    DETAIL = "User not authenticated"

    def __init__(self) -> None:
        super().__init__(headers={"WWW-Authenticate": "Bearer"})
