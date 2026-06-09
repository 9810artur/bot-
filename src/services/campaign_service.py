"""Campaign service."""

from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import CampaignStatus
from src.repositories.campaign import CampaignRepository


class CampaignService:
    """Campaign service for business logic."""

    def __init__(self, session: AsyncSession):
        """Initialize service with repositories."""
        self.campaign_repo = CampaignRepository(session)
        self.session = session

    async def create_campaign(
        self,
        advertiser_id: int,
        title: str,
        city: str,
        budget: float,
        campaign_date: datetime,
        description: str | None = None,
        required_influencers: int = 1,
    ):
        """Create new campaign."""
        campaign = await self.campaign_repo.create(
            advertiser_id=advertiser_id,
            title=title,
            description=description,
            city=city,
            budget=budget,
            required_influencers=required_influencers,
            campaign_date=campaign_date,
            status=CampaignStatus.DRAFT,
        )
        await self.session.commit()
        return campaign

    async def get_campaign(self, campaign_id: int):
        """Get campaign by ID."""
        return await self.campaign_repo.get_by_id(campaign_id)

    async def get_advertiser_campaigns(self, advertiser_id: int):
        """Get all campaigns by advertiser."""
        return await self.campaign_repo.get_by_advertiser_id(advertiser_id)

    async def get_active_campaigns(self):
        """Get all active campaigns."""
        return await self.campaign_repo.get_active_campaigns()

    async def update_campaign(self, campaign_id: int, **kwargs):
        """Update campaign."""
        campaign = await self.campaign_repo.update(campaign_id, **kwargs)
        await self.session.commit()
        return campaign

    async def activate_campaign(self, campaign_id: int):
        """Activate campaign."""
        return await self.update_campaign(campaign_id, status=CampaignStatus.ACTIVE)

    async def delete_campaign(self, campaign_id: int):
        """Delete campaign."""
        result = await self.campaign_repo.delete(campaign_id)
        await self.session.commit()
        return result
