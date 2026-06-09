"""Campaign model."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
import enum

from src.database.base import Base


class CampaignStatus(str, enum.Enum):
    """Campaign status enum."""

    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Campaign(Base):
    """Campaign model."""

    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    advertiser_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    city = Column(String(255), nullable=False)
    budget = Column(Float, nullable=False)
    required_influencers = Column(Integer, default=1)
    campaign_date = Column(DateTime, nullable=False)
    status = Column(Enum(CampaignStatus), default=CampaignStatus.DRAFT, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    advertiser = relationship(
        "User",
        back_populates="campaigns",
        foreign_keys="Campaign.advertiser_id",
    )
    applications = relationship(
        "Application",
        back_populates="campaign",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Campaign(id={self.id}, advertiser_id={self.advertiser_id}, title={self.title})>"
