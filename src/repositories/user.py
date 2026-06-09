"""User repository."""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.database.models import User, UserRole


class UserRepository:
    """User repository for data access."""

    def __init__(self, session: AsyncSession):
        """Initialize repository with database session."""
        self.session = session

    async def create(self, telegram_id: int, full_name: str, role: UserRole, **kwargs) -> User:
        """Create new user."""
        user = User(
            telegram_id=telegram_id,
            full_name=full_name,
            role=role,
            **kwargs,
        )
        self.session.add(user)
        await self.session.flush()
        return user

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        """Get user by telegram ID."""
        stmt = select(User).where(User.telegram_id == telegram_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_by_id(self, user_id: int) -> User | None:
        """Get user by ID."""
        stmt = select(User).where(User.id == user_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def update(self, user_id: int, **kwargs) -> User | None:
        """Update user."""
        user = await self.get_by_id(user_id)
        if user:
            for key, value in kwargs.items():
                if hasattr(user, key) and value is not None:
                    setattr(user, key, value)
            await self.session.flush()
        return user

    async def exists(self, telegram_id: int) -> bool:
        """Check if user exists."""
        stmt = select(User).where(User.telegram_id == telegram_id)
        result = await self.session.execute(stmt)
        return result.scalars().first() is not None
