from fastapi import status

from src.exceptions import DetailedWSException


class RoomNotFoundWS(DetailedWSException):
    reason = "Room not found"


class PermissionDeniedWS(DetailedWSException):
    reason = "Permission denied"


class NotAuthenticatedWS(DetailedWSException):
    reason = "Not authenticated"
