"""Campaign repository."""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.database.models import Campaign, CampaignStatus


class CampaignRepository:
    """Campaign repository for data access."""

    def __init__(self, session: AsyncSession):
        """Initialize repository with database session."""
        self.session = session

    async def create(self, advertiser_id: int, **kwargs) -> Campaign:
        """Create new campaign."""
        campaign = Campaign(advertiser_id=advertiser_id, **kwargs)
        self.session.add(campaign)
        await self.session.flush()
        return campaign

    async def get_by_id(self, campaign_id: int) -> Campaign | None:
        """Get campaign by ID."""
        stmt = select(Campaign).where(Campaign.id == campaign_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_by_advertiser_id(self, advertiser_id: int) -> list[Campaign]:
        """Get all campaigns by advertiser ID."""
        stmt = select(Campaign).where(Campaign.advertiser_id == advertiser_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_active_campaigns(self) -> list[Campaign]:
        """Get all active campaigns."""
        stmt = select(Campaign).where(Campaign.status == CampaignStatus.ACTIVE)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update(self, campaign_id: int, **kwargs) -> Campaign | None:
        """Update campaign."""
        campaign = await self.get_by_id(campaign_id)
        if campaign:
            for key, value in kwargs.items():
                if hasattr(campaign, key) and value is not None:
                    setattr(campaign, key, value)
            await self.session.flush()
        return campaign

    async def delete(self, campaign_id: int) -> bool:
        """Delete campaign."""
        campaign = await self.get_by_id(campaign_id)
        if campaign:
            await self.session.delete(campaign)
            await self.session.flush()
            return True
        return False
