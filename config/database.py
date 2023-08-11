import os
from pathlib import Path

from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class DatabaseSettings(BaseSettings):
    username: str
    password: str
    host: str
    port: str
    name: str


env_path: str = os.path.join(Path(__file__).resolve().parent.parent, '.env')
db_settings = DatabaseSettings(_env_file=env_path)

SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{db_settings.username}:{db_settings.password}@" \
                          f"{db_settings.host}:{db_settings.port}/{db_settings.name}"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
