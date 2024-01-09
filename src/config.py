import os
from datetime import timedelta

from pydantic_settings import BaseSettings


class MediaSettings(BaseSettings):
    MAX_FILE_SIZE: int = 1024 * 1024 * 50
    ALLOWED_IMAGE_EXTENSIONS: list = ['jpg', 'jpeg', 'png']
    ALLOWED_FILE_EXTENSIONS: list = []
    ALLOWED_EXTENSIONS: list = ALLOWED_IMAGE_EXTENSIONS + ALLOWED_FILE_EXTENSIONS
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    MEDIA_ROOT: str = "media"
    MEDIA_DIR: str = os.path.join(BASE_DIR, MEDIA_ROOT)


class Settings(BaseSettings):
    PSQL_DATABASE_HOST: str
    PSQL_DATABASE_NAME: str
    PSQL_DATABASE_USER: str
    PSQL_DATABASE_PASSWORD: str
    SECRET_KEY: str
    DEFAULT_CHUNK_SIZE: int = 1024 * 1024 * 50
    JWT_AUTH_ACCESS_COOKIE: str = 'access'
    JWT_AUTH_REFRESH_COOKIE: str = 'refresh'
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    ACCESS_TOKEN_LIFETIME: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    REFRESH_TOKEN_LIFETIME: timedelta = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    MEDIA: MediaSettings = MediaSettings()

    class Config:
        env_file: str = '../.env'
        env_file_encoding: str = 'utf-8'
        case_sensitive: bool = True


settings = Settings()
