"""Application repository."""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.database.models import Application, ApplicationStatus


class ApplicationRepository:
    """Application repository for data access."""

    def __init__(self, session: AsyncSession):
        """Initialize repository with database session."""
        self.session = session

    async def create(self, campaign_id: int, influencer_id: int) -> Application:
        """Create new application."""
        application = Application(campaign_id=campaign_id, influencer_id=influencer_id)
        self.session.add(application)
        await self.session.flush()
        return application

    async def get_by_id(self, application_id: int) -> Application | None:
        """Get application by ID."""
        stmt = select(Application).where(Application.id == application_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_by_campaign_id(self, campaign_id: int) -> list[Application]:
        """Get all applications for campaign."""
        stmt = select(Application).where(Application.campaign_id == campaign_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_influencer_id(self, influencer_id: int) -> list[Application]:
        """Get all applications by influencer."""
        stmt = select(Application).where(Application.influencer_id == influencer_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_campaign_and_influencer(
        self, campaign_id: int, influencer_id: int
    ) -> Application | None:
        """Get application by campaign and influencer."""
        stmt = select(Application).where(
            (Application.campaign_id == campaign_id)
            & (Application.influencer_id == influencer_id)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def update(self, application_id: int, **kwargs) -> Application | None:
        """Update application."""
        application = await self.get_by_id(application_id)
        if application:
            for key, value in kwargs.items():
                if hasattr(application, key) and value is not None:
                    setattr(application, key, value)
            await self.session.flush()
        return application

    async def accept(self, application_id: int) -> Application | None:
        """Accept application."""
        return await self.update(application_id, status=ApplicationStatus.ACCEPTED)

    async def reject(self, application_id: int) -> Application | None:
        """Reject application."""
        return await self.update(application_id, status=ApplicationStatus.REJECTED)
