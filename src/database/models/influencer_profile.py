"""InfluencerProfile model."""

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from src.database.base import Base


class InfluencerProfile(Base):
    """InfluencerProfile model."""

    __tablename__ = "influencer_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    niche = Column(String(255), nullable=True)
    followers_count = Column(Integer, default=0)
    instagram_link = Column(String(500), nullable=True)
    tiktok_link = Column(String(500), nullable=True)
    telegram_link = Column(String(500), nullable=True)
    advertising_price = Column(Float, default=0.0)

    # Relationships
    user = relationship("User", back_populates="influencer_profile")

    def __repr__(self) -> str:
        return f"<InfluencerProfile(id={self.id}, user_id={self.user_id}, niche={self.niche})>"
