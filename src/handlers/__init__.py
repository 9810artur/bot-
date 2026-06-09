"""Handlers module for LocalAdsBot."""

from src.handlers.registration import router as registration_router
from src.handlers.influencer import router as influencer_router
from src.handlers.advertiser import router as advertiser_router

__all__ = [
    "registration_router",
    "influencer_router",
    "advertiser_router",
]
