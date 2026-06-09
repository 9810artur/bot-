"""Application model."""

from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum

from src.database.base import Base


class ApplicationStatus(str, enum.Enum):
    """Application status enum."""

    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Application(Base):
    """Application model."""

    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False)
    influencer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.PENDING, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    campaign = relationship("Campaign", back_populates="applications")
    influencer = relationship(
        "User",
        back_populates="applications",
        foreign_keys="Application.influencer_id",
    )

    def __repr__(self) -> str:
        return f"<Application(id={self.id}, campaign_id={self.campaign_id}, influencer_id={self.influencer_id})>"
