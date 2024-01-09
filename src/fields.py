from typing import Union

from sqlalchemy import String, TypeDecorator, Dialect

from src.config import settings


class ImageField(TypeDecorator):
    impl = String

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def process_bind_param(self, value: str, dialect: Dialect) -> Union[str, None]:
        return value if value else None

    def process_result_value(self, value, dialect: Dialect) -> Union[str, None]:
        if value is not None:
            return value.replace(settings.MEDIA.BASE_DIR, "")
        else:
            return None
