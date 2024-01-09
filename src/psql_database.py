from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.PSQL_DATABASE_USER}:{settings.PSQL_DATABASE_PASSWORD}" \
                          f"@{settings.PSQL_DATABASE_HOST}/{settings.PSQL_DATABASE_NAME}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
