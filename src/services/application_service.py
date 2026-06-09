"""Application service."""

from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.application import ApplicationRepository


class ApplicationService:
    """Application service for business logic."""

    def __init__(self, session: AsyncSession):
        """Initialize service with repositories."""
        self.app_repo = ApplicationRepository(session)
        self.session = session

    async def create_application(self, campaign_id: int, influencer_id: int):
        """Create new application."""
        existing = await self.app_repo.get_by_campaign_and_influencer(
            campaign_id, influencer_id
        )
        if existing:
            return None

        application = await self.app_repo.create(campaign_id, influencer_id)
        await self.session.commit()
        return application

    async def get_application(self, application_id: int):
        """Get application by ID."""
        return await self.app_repo.get_by_id(application_id)

    async def get_campaign_applications(self, campaign_id: int):
        """Get all applications for campaign."""
        return await self.app_repo.get_by_campaign_id(campaign_id)

    async def get_influencer_applications(self, influencer_id: int):
        """Get all applications by influencer."""
        return await self.app_repo.get_by_influencer_id(influencer_id)

    async def accept_application(self, application_id: int):
        """Accept application."""
        application = await self.app_repo.accept(application_id)
        await self.session.commit()
        return application

    async def reject_application(self, application_id: int):
        """Reject application."""
        application = await self.app_repo.reject(application_id)
        await self.session.commit()
        return application
