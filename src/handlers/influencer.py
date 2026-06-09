"""Influencer handlers."""

import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession

from src.states.influencer_profile import InfluencerProfileStates
from src.states.campaign import CampaignCreationStates
from src.keyboards import get_influencer_menu_keyboard, get_skip_keyboard
from src.services.user_service import UserService
from src.services.influencer_profile_service import InfluencerProfileService
from src.services.campaign_service import CampaignService
from src.services.application_service import ApplicationService
from src.database import async_session_factory

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command("influencer"))
async def influencer_menu(message: Message) -> None:
    """Show influencer menu."""
    await message.answer(
        "📱 Меню блогера",
        reply_markup=get_influencer_menu_keyboard(),
    )


@router.message(F.text == "👤 Моя анкета")
async def my_profile(message: Message, state: FSMContext) -> None:
    """Show influencer profile or start creation."""
    async with async_session_factory() as session:
        profile_service = InfluencerProfileService(session)
        profile = await profile_service.get_profile(message.from_user.id)

    if profile:
        text = (
            f"👤 Твоя анкета:\n\n"
            f"Ниша: {profile.niche or 'Не указана'}\n"
            f"Подписчики: {profile.followers_count}\n"
            f"Instagram: {profile.instagram_link or 'Не указана'}\n"
            f"TikTok: {profile.tiktok_link or 'Не указана'}\n"
            f"Telegram: {profile.telegram_link or 'Не указана'}\n"
            f"Цена: ${profile.advertising_price}"
        )
        await message.answer(text)
    else:
        await message.answer(
            "У тебя ещё нет анкеты. Давай её создадим!\n"
            "Введи свою нишу (область деятельности):"
        )
        await state.set_state(InfluencerProfileStates.waiting_for_niche)


@router.message(InfluencerProfileStates.waiting_for_niche)
async def get_niche(message: Message, state: FSMContext) -> None:
    """Handle niche input."""
    await state.update_data(niche=message.text)
    await state.set_state(InfluencerProfileStates.waiting_for_followers)
    await message.answer(
        "Сколько подписчиков у тебя? (введи число):"
    )


@router.message(InfluencerProfileStates.waiting_for_followers)
async def get_followers(message: Message, state: FSMContext) -> None:
    """Handle followers count input."""
    try:
        followers = int(message.text)
        await state.update_data(followers_count=followers)
    except ValueError:
        await message.answer("❌ Введи число подписчиков:")
        return

    await state.set_state(InfluencerProfileStates.waiting_for_instagram)
    await message.answer(
        "Ссылка на Instagram (или '-' для пропуска):",
        reply_markup=get_skip_keyboard(),
    )


@router.message(InfluencerProfileStates.waiting_for_instagram)
async def get_instagram(message: Message, state: FSMContext) -> None:
    """Handle Instagram link input."""
    instagram = None if message.text == "-" else message.text
    await state.update_data(instagram_link=instagram)
    await state.set_state(InfluencerProfileStates.waiting_for_tiktok)
    await message.answer(
        "Ссылка на TikTok (или '-' для пропуска):"
    )


@router.message(InfluencerProfileStates.waiting_for_tiktok)
async def get_tiktok(message: Message, state: FSMContext) -> None:
    """Handle TikTok link input."""
    tiktok = None if message.text == "-" else message.text
    await state.update_data(tiktok_link=tiktok)
    await state.set_state(InfluencerProfileStates.waiting_for_telegram)
    await message.answer(
        "Ссылка на Telegram (или '-' для пропуска):"
    )


@router.message(InfluencerProfileStates.waiting_for_telegram)
async def get_telegram(message: Message, state: FSMContext) -> None:
    """Handle Telegram link input."""
    telegram = None if message.text == "-" else message.text
    await state.update_data(telegram_link=telegram)
    await state.set_state(InfluencerProfileStates.waiting_for_price)
    await message.answer(
        "Твоя цена за одну рекламу (в $):"
    )


@router.message(InfluencerProfileStates.waiting_for_price)
async def get_price(message: Message, state: FSMContext) -> None:
    """Handle price input and complete profile creation."""
    try:
        price = float(message.text)
    except ValueError:
        await message.answer("❌ Введи корректную цену:")
        return

    data = await state.get_data()

    async with async_session_factory() as session:
        profile_service = InfluencerProfileService(session)
        profile = await profile_service.create_profile(
            user_id=message.from_user.id,
            niche=data["niche"],
            followers_count=data["followers_count"],
            instagram_link=data.get("instagram_link"),
            tiktok_link=data.get("tiktok_link"),
            telegram_link=data.get("telegram_link"),
            advertising_price=price,
        )

    if profile:
        logger.info(f"Profile created for user: {message.from_user.id}")
        await message.answer(
            "✅ Анкета создана!\n"
            "Теперь ты можешь просматривать кампании и подавать заявки."
        )
    else:
        await message.answer("❌ Ошибка при создании анкеты.")

    await state.clear()


@router.message(F.text == "📢 Просмотр кампаний")
async def view_campaigns(message: Message) -> None:
    """Show available campaigns."""
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
        await message.answer(text)
    else:
        await message.answer("❌ Доступных кампаний не найдено.")


@router.message(F.text == "📋 Мои заявки")
async def my_applications(message: Message) -> None:
    """Show influencer's applications."""
    async with async_session_factory() as session:
        app_service = ApplicationService(session)
        applications = await app_service.get_influencer_applications(message.from_user.id)

    if applications:
        text = "📋 Твои заявки:\n\n"
        for app in applications:
            status_text = {
                "pending": "⏳ На рассмотрении",
                "accepted": "✅ Принята",
                "rejected": "❌ Отклонена",
            }.get(app.status, app.status)
            text += f"Кампания ID {app.campaign_id}: {status_text}\n"
        await message.answer(text)
    else:
        await message.answer("❌ У тебя нет заявок.")
