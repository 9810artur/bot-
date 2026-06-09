"""User model."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
import enum

from src.database.base import Base


class UserRole(str, enum.Enum):
    """User role enum."""

    ADVERTISER = "advertiser"
    INFLUENCER = "influencer"
    ADMIN = "admin"


class User(Base):
    """User model."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True, nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.INFLUENCER)
    full_name = Column(String(255), nullable=False)
    username = Column(String(255), nullable=True, unique=True, index=True)
    city = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    influencer_profile = relationship(
        "InfluencerProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
    campaigns = relationship(
        "Campaign",
        back_populates="advertiser",
        foreign_keys="Campaign.advertiser_id",
        cascade="all, delete-orphan",
    )
    applications = relationship(
        "Application",
        back_populates="influencer",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, telegram_id={self.telegram_id}, role={self.role})>"
