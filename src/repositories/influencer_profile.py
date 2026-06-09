"""Influencer profile repository."""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.database.models import InfluencerProfile


class InfluencerProfileRepository:
    """InfluencerProfile repository for data access."""

    def __init__(self, session: AsyncSession):
        """Initialize repository with database session."""
        self.session = session

    async def create(self, user_id: int, **kwargs) -> InfluencerProfile:
        """Create new influencer profile."""
        profile = InfluencerProfile(user_id=user_id, **kwargs)
        self.session.add(profile)
        await self.session.flush()
        return profile

    async def get_by_user_id(self, user_id: int) -> InfluencerProfile | None:
        """Get influencer profile by user ID."""
        stmt = select(InfluencerProfile).where(InfluencerProfile.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_by_id(self, profile_id: int) -> InfluencerProfile | None:
        """Get influencer profile by ID."""
        stmt = select(InfluencerProfile).where(InfluencerProfile.id == profile_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def update(self, user_id: int, **kwargs) -> InfluencerProfile | None:
        """Update influencer profile."""
        profile = await self.get_by_user_id(user_id)
        if profile:
            for key, value in kwargs.items():
                if hasattr(profile, key) and value is not None:
                    setattr(profile, key, value)
            await self.session.flush()
        return profile

    async def exists(self, user_id: int) -> bool:
        """Check if influencer profile exists."""
        stmt = select(InfluencerProfile).where(InfluencerProfile.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalars().first() is not None
