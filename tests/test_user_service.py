"""Tests for user service."""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.database.models import Base, UserRole
from src.services.user_service import UserService


@pytest.fixture
async def db_session():
    """Create test database session."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)

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


@pytest.mark.asyncio
async def test_register_user(db_session):
    """Test user registration."""
    service = UserService(db_session)

    user = await service.register_user(
        telegram_id=123456789,
        full_name="Test User",
        role=UserRole.INFLUENCER,
        username="testuser",
        city="Moscow",
    )

    assert user is not None
    assert user.telegram_id == 123456789
    assert user.full_name == "Test User"
    assert user.role == UserRole.INFLUENCER


@pytest.mark.asyncio
async def test_get_user(db_session):
    """Test getting user."""
    service = UserService(db_session)

    # Create user
    user = await service.register_user(
        telegram_id=123456789,
        full_name="Test User",
        role=UserRole.INFLUENCER,
    )

    # Get user
    retrieved_user = await service.get_user(123456789)

    assert retrieved_user is not None
    assert retrieved_user.id == user.id
    assert retrieved_user.telegram_id == 123456789
