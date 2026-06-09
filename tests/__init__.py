"""Test utilities and fixtures."""

import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.database.models import Base


async def get_test_session():
    """Create test database session."""
    # Use SQLite for testing
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    TestingSessionLocal = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with TestingSessionLocal() as session:
        yield session

    await engine.dispose()
