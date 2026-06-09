"""Callback handlers for campaigns and applications."""

import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import async_session_factory
from src.services.campaign_service import CampaignService
from src.services.application_service import ApplicationService
from src.keyboards import get_campaign_details_keyboard, get_application_action_keyboard

router = Router()
logger = logging.getLogger(__name__)


@router.callback_query(F.data.startswith("campaign_"))
async def show_campaign_details(callback: CallbackQuery) -> None:
    """Show campaign details."""
    try:
        campaign_id = int(callback.data.split("_")[1])
    except (ValueError, IndexError):
        await callback.answer("❌ Invalid campaign ID")
        return

    async with async_session_factory() as session:
        campaign_service = CampaignService(session)
        campaign = await campaign_service.get_campaign(campaign_id)

    if not campaign:
        await callback.answer("❌ Campaign not found")
        return

    text = (
        f"📢 {campaign.title}\n\n"
        f"Описание: {campaign.description or 'Не указано'}\n"
        f"Город: {campaign.city}\n"
        f"Бюджет: ${campaign.budget}\n"
        f"Нужно блогеров: {campaign.required_influencers}\n"
        f"Дата: {campaign.campaign_date.strftime('%d.%m.%Y %H:%M')}\n"
        f"Статус: {campaign.status}"
    )

    await callback.message.edit_text(
        text,
        reply_markup=get_campaign_details_keyboard(campaign_id),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("apply_campaign_"))
async def apply_to_campaign(callback: CallbackQuery) -> None:
    """Apply to campaign as influencer."""
    try:
        campaign_id = int(callback.data.split("_")[2])
    except (ValueError, IndexError):
        await callback.answer("❌ Invalid campaign ID")
        return

    async with async_session_factory() as session:
        app_service = ApplicationService(session)
        application = await app_service.create_application(
            campaign_id=campaign_id,
            influencer_id=callback.from_user.id,
        )

    if application:
        await callback.answer("✅ Заявка подана успешно!")
        await callback.message.answer(
            f"📋 Ваша заявка на кампанию (ID {campaign_id}) принята.\n"
            "Ожидайте решения бизнеса."
        )
        logger.info(
            f"Application created: {application.id} "
            f"(campaign_id={campaign_id}, influencer_id={callback.from_user.id})"
        )
    else:
        await callback.answer("❌ Вы уже подали заявку на эту кампанию")


@router.callback_query(F.data == "back_to_campaigns")
async def back_to_campaigns(callback: CallbackQuery) -> None:
    """Go back to campaigns list."""
    async with async_session_factory() as session:
        campaign_service = CampaignService(session)
        campaigns = await campaign_service.get_active_campaigns()

    if campaigns:
        text = "📢 Доступные кампании:\n\n"
        for idx, campaign in enumerate(campaigns[:5], 1):
            text += (
                f"{idx}. {campaign.title}\n"
                f"   Город: {campaign.city}\n"
                f"   Бюджет: ${campaign.budget}\n\n"
            )
        await callback.message.edit_text(text)
    else:
        await callback.message.edit_text("❌ Доступных кампаний не найдено.")

    await callback.answer()


@router.callback_query(F.data.startswith("accept_application_"))
async def accept_application(callback: CallbackQuery) -> None:
    """Accept application."""
    try:
        application_id = int(callback.data.split("_")[2])
    except (ValueError, IndexError):
        await callback.answer("❌ Invalid application ID")
        return

    async with async_session_factory() as session:
        app_service = ApplicationService(session)
        application = await app_service.accept_application(application_id)

    if application:
        await callback.answer("✅ Заявка принята!")
        await callback.message.edit_text(
            f"📋 Заявка от блогера (ID {application.influencer_id}) принята!\n"
            "Статус обновлён."
        )
        logger.info(f"Application accepted: {application_id}")
    else:
        await callback.answer("❌ Заявка не найдена")


@router.callback_query(F.data.startswith("reject_application_"))
async def reject_application(callback: CallbackQuery) -> None:
    """Reject application."""
    try:
        application_id = int(callback.data.split("_")[2])
    except (ValueError, IndexError):
        await callback.answer("❌ Invalid application ID")
        return

    async with async_session_factory() as session:
        app_service = ApplicationService(session)
        application = await app_service.reject_application(application_id)

    if application:
        await callback.answer("✅ Заявка отклонена")
        await callback.message.edit_text(
            f"📋 Заявка от блогера (ID {application.influencer_id}) отклонена.\n"
            "Статус обновлён."
        )
        logger.info(f"Application rejected: {application_id}")
    else:
        await callback.answer("❌ Заявка не найдена")


@router.callback_query(F.data == "confirm")
async def confirm_action(callback: CallbackQuery) -> None:
    """Confirm action."""
    await callback.answer("✅ Действие подтверждено")


@router.callback_query(F.data == "cancel")
async def cancel_action(callback: CallbackQuery) -> None:
    """Cancel action."""
    await callback.answer("❌ Действие отменено")
    await callback.message.delete()


@router.callback_query(F.data == "skip")
async def skip_action(callback: CallbackQuery) -> None:
    """Skip optional field."""
    await callback.answer("➡️ Пропущено")
