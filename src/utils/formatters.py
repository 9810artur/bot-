"""Utility formatters."""

from datetime import datetime
from src.database.models import ApplicationStatus, CampaignStatus, UserRole


def format_date(dt: datetime) -> str:
    """Format datetime to readable string."""
    return dt.strftime("%d.%m.%Y %H:%M")


def format_status(status: str, status_type: str = "application") -> str:
    """Format status to readable string.

    Args:
        status: Status value
        status_type: Type of status (application, campaign, role)

    Returns:
        Formatted status string
    """
    if status_type == "application":
        statuses = {
            "pending": "⏳ На рассмотрении",
            "accepted": "✅ Принята",
            "rejected": "❌ Отклонена",
            "completed": "🎉 Завершена",
        }
    elif status_type == "campaign":
        statuses = {
            "draft": "📝 Черновик",
            "active": "🟢 Активна",
            "paused": "⏸️ На паузе",
            "completed": "🎉 Завершена",
            "cancelled": "❌ Отменена",
        }
    elif status_type == "role":
        statuses = {
            "advertiser": "💼 Бизнес",
            "influencer": "📱 Блогер",
            "admin": "👨‍💼 Администратор",
        }
    else:
        return status

    return statuses.get(status, status)


def format_price(price: float) -> str:
    """Format price to readable string."""
    return f"${price:.2f}"


def format_campaign_info(campaign) -> str:
    """Format campaign info to readable string."""
    return (
        f"📢 {campaign.title}\n"
        f"Описание: {campaign.description or 'Не указано'}\n"
        f"Город: {campaign.city}\n"
        f"Бюджет: {format_price(campaign.budget)}\n"
        f"Нужно блогеров: {campaign.required_influencers}\n"
        f"Дата: {format_date(campaign.campaign_date)}\n"
        f"Статус: {format_status(campaign.status, 'campaign')}"
    )
