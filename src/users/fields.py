from typing import Union

from sqlalchemy import String, TypeDecorator, Dialect

from src.users.security import PasswordHash


class Password(TypeDecorator):
    impl = String

    def __init__(self, rounds: int = 12, **kwargs):
        self.rounds = rounds
        super().__init__(**kwargs)

    def process_bind_param(self, value: str, dialect: Dialect) -> Union[str, None]:
        return self._convert(value).hash if value else None

    def process_result_value(self, value, dialect: Dialect) -> Union['PasswordHash', None]:
        if value is not None:
            return PasswordHash(bytes(value, 'utf-8'))

    def validator(self, password: str) -> Union['PasswordHash', None]:
        return self._convert(password)

    def _convert(self, value: Union[str, 'PasswordHash']) -> Union['PasswordHash', None]:
        if isinstance(value, PasswordHash) or value is None:
            return value
        elif isinstance(value, str):
            return PasswordHash.new(value, self.rounds)
        else:
            raise TypeError(
                f'Cannot convert {type(value)} to a PasswordHash'
            )
