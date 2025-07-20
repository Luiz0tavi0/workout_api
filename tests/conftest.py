from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from testcontainers.postgres import PostgresContainer

from workout_api.configs.database import get_session
from workout_api.contrib.models import BaseModel
from workout_api.main import app


@pytest.fixture(scope='session')
def engine():
    with PostgresContainer('postgres:17', 5548, driver='psycopg') as postgres:
        database_url = postgres.get_connection_url()
        _engine = create_async_engine(database_url)
        yield _engine


@pytest_asyncio.fixture(scope='function')
async def session(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as _session:
        yield _session
    # teardown
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)


@pytest_asyncio.fixture(scope='function')
async def client(session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    def override_session():
        yield session

    app.dependency_overrides[get_session] = override_session

    async with AsyncClient(base_url='http://localhost:8000') as client_test:
        yield client_test

    app.dependency_overrides.clear()
