from abc import ABC
from typing import AsyncGenerator

import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker

from config.database import Base, get_session
from main import app


class BaseTest(ABC):

    SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:masterkey@localhost:5432/test"

    @pytest_asyncio.fixture(scope='function')
    async def async_db_engine(self) -> AsyncGenerator[AsyncEngine, None]:
        engine: AsyncEngine = create_async_engine(self.SQLALCHEMY_DATABASE_URL, echo=True)
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        yield engine

        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    @pytest_asyncio.fixture(scope="function")
    async def test_db_session(self, async_db_engine) -> AsyncGenerator[AsyncSession, None]:
        async_session: AsyncSession = sessionmaker(
            expire_on_commit=False,
            autocommit=False,
            autoflush=False,
            bind=async_db_engine,
            class_=AsyncSession,
        )

        async with async_session() as session:
            await session.begin()

            yield session

            await session.rollback()
            await session.commit()

    @pytest_asyncio.fixture(scope="function")
    async def client(self, test_db_session) -> AsyncGenerator[AsyncClient, None]:
        app.dependency_overrides[get_session] = lambda: test_db_session
        async with AsyncClient(app=app, base_url='http://localhost') as client:
            yield client
