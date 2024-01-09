from src.exceptions import NotAuthenticated


class IncorrectUsernameOrPassword(NotAuthenticated):
    DETAIL = "Incorrect username or password"
