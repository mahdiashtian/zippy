from src.exceptions import NotFound, BadRequest
from src.users.constants import ErrorCode


class UserDoesNotExist(NotFound):
    DETAIL = ErrorCode.USER_NOT_FOUND


class UserAlreadyExists(BadRequest):
    DETAIL = ErrorCode.USER_ALREADY_EXISTS
