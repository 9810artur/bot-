"""Influencer profile service."""

from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.influencer_profile import InfluencerProfileRepository


class InfluencerProfileService:
    """Influencer profile service for business logic."""

    def __init__(self, session: AsyncSession):
        """Initialize service with repositories."""
        self.profile_repo = InfluencerProfileRepository(session)
        self.session = session

    async def create_profile(
        self,
        user_id: int,
        niche: str | None = None,
        followers_count: int = 0,
        instagram_link: str | None = None,
        tiktok_link: str | None = None,
        telegram_link: str | None = None,
        advertising_price: float = 0.0,
    ):
        """Create new influencer profile."""
        if await self.profile_repo.exists(user_id):
            return None

        profile = await self.profile_repo.create(
            user_id=user_id,
            niche=niche,
            followers_count=followers_count,
            instagram_link=instagram_link,
            tiktok_link=tiktok_link,
            telegram_link=telegram_link,
            advertising_price=advertising_price,
        )
        await self.session.commit()
        return profile

    async def get_profile(self, user_id: int):
        """Get influencer profile."""
        return await self.profile_repo.get_by_user_id(user_id)

    async def update_profile(self, user_id: int, **kwargs):
        """Update influencer profile."""
        profile = await self.profile_repo.update(user_id, **kwargs)
        await self.session.commit()
        return profile
