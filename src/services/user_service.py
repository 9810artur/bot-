"""User service."""

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import UserRole
from src.repositories.user import UserRepository
from src.repositories.influencer_profile import InfluencerProfileRepository


class UserService:
    """User service for business logic."""

    def __init__(self, session: AsyncSession):
        """Initialize service with repositories."""
        self.user_repo = UserRepository(session)
        self.profile_repo = InfluencerProfileRepository(session)
        self.session = session

    async def register_user(
        self,
        telegram_id: int,
        full_name: str,
        role: UserRole,
        username: str | None = None,
        city: str | None = None,
    ):
        """Register new user."""
        if await self.user_repo.exists(telegram_id):
            return None

        user = await self.user_repo.create(
            telegram_id=telegram_id,
            full_name=full_name,
            role=role,
            username=username,
            city=city,
        )
        await self.session.commit()
        return user

    async def get_user(self, telegram_id: int):
        """Get user by telegram ID."""
        return await self.user_repo.get_by_telegram_id(telegram_id)

    async def update_user(self, user_id: int, **kwargs):
        """Update user."""
        user = await self.user_repo.update(user_id, **kwargs)
        await self.session.commit()
        return user

    async def is_influencer(self, user_id: int) -> bool:
        """Check if user is influencer."""
        return await self.profile_repo.exists(user_id)

    async def has_profile(self, user_id: int) -> bool:
        """Check if influencer has profile."""
        return await self.profile_repo.exists(user_id)
