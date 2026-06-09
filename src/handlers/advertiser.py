"""Advertiser handlers."""

import logging
from datetime import datetime
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession

from src.states.campaign import CampaignCreationStates
from src.keyboards import get_advertiser_menu_keyboard
from src.services.campaign_service import CampaignService
from src.services.application_service import ApplicationService
from src.database import async_session_factory

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command("advertiser"))
async def advertiser_menu(message: Message) -> None:
    """Show advertiser menu."""
    await message.answer(
        "💼 Меню бизнеса",
        reply_markup=get_advertiser_menu_keyboard(),
    )


@router.message(F.text == "➕ Создать кампанию")
async def create_campaign_start(message: Message, state: FSMContext) -> None:
    """Start campaign creation."""
    await state.set_state(CampaignCreationStates.waiting_for_title)
    await message.answer("Введи название кампании:")


@router.message(CampaignCreationStates.waiting_for_title)
async def get_campaign_title(message: Message, state: FSMContext) -> None:
    """Handle campaign title input."""
    await state.update_data(title=message.text)
    await state.set_state(CampaignCreationStates.waiting_for_description)
    await message.answer("Введи описание кампании:")


@router.message(CampaignCreationStates.waiting_for_description)
async def get_campaign_description(message: Message, state: FSMContext) -> None:
    """Handle campaign description input."""
    await state.update_data(description=message.text)
    await state.set_state(CampaignCreationStates.waiting_for_city)
    await message.answer("Введи город для кампании:")


@router.message(CampaignCreationStates.waiting_for_city)
async def get_campaign_city(message: Message, state: FSMContext) -> None:
    """Handle campaign city input."""
    await state.update_data(city=message.text)
    await state.set_state(CampaignCreationStates.waiting_for_budget)
    await message.answer("Введи бюджет кампании (в $):")


@router.message(CampaignCreationStates.waiting_for_budget)
async def get_campaign_budget(message: Message, state: FSMContext) -> None:
    """Handle campaign budget input."""
    try:
        budget = float(message.text)
        await state.update_data(budget=budget)
    except ValueError:
        await message.answer("❌ Введи корректную сумму:")
        return

    await state.set_state(CampaignCreationStates.waiting_for_required_influencers)
    await message.answer("Сколько блогеров нужно для кампании?")


@router.message(CampaignCreationStates.waiting_for_required_influencers)
async def get_required_influencers(message: Message, state: FSMContext) -> None:
    """Handle required influencers count input."""
    try:
        count = int(message.text)
        await state.update_data(required_influencers=count)
    except ValueError:
        await message.answer("❌ Введи число:")
        return

    await state.set_state(CampaignCreationStates.waiting_for_campaign_date)
    await message.answer(
        "Введи дату кампании (в формате YYYY-MM-DD HH:MM):\n"
        "Пример: 2026-06-15 10:30"
    )


@router.message(CampaignCreationStates.waiting_for_campaign_date)
async def get_campaign_date(message: Message, state: FSMContext) -> None:
    """Handle campaign date input and complete campaign creation."""
    try:
        campaign_date = datetime.strptime(message.text, "%Y-%m-%d %H:%M")
    except ValueError:
        await message.answer(
            "❌ Неверный формат даты.\n"
            "Используй формат: YYYY-MM-DD HH:MM"
        )
        return

    data = await state.get_data()

    async with async_session_factory() as session:
        campaign_service = CampaignService(session)
        campaign = await campaign_service.create_campaign(
            advertiser_id=message.from_user.id,
            title=data["title"],
            description=data["description"],
            city=data["city"],
            budget=data["budget"],
            required_influencers=data["required_influencers"],
            campaign_date=campaign_date,
        )

    if campaign:
        logger.info(f"Campaign created: {campaign.id}")
        await message.answer(
            f"✅ Кампания создана!\n"
            f"ID: {campaign.id}\n"
            f"Название: {campaign.title}\n"
            f"Статус: Черновик"
        )
    else:
        await message.answer("❌ Ошибка при создании кампании.")

    await state.clear()


@router.message(F.text == "📊 Мои кампании")
async def my_campaigns(message: Message) -> None:
    """Show advertiser's campaigns."""
    async with async_session_factory() as session:
        campaign_service = CampaignService(session)
        campaigns = await campaign_service.get_advertiser_campaigns(message.from_user.id)

    if campaigns:
        text = "📊 Твои кампании:\n\n"
        for campaign in campaigns:
            text += (
                f"ID: {campaign.id}\n"
                f"Название: {campaign.title}\n"
                f"Город: {campaign.city}\n"
                f"Бюджет: ${campaign.budget}\n"
                f"Статус: {campaign.status}\n\n"
            )
        await message.answer(text)
    else:
        await message.answer("❌ У тебя нет кампаний.")


@router.message(F.text == "👥 Заявки")
async def view_applications(message: Message) -> None:
    """Show applications for advertiser's campaigns."""
    async with async_session_factory() as session:
        campaign_service = CampaignService(session)
        campaigns = await campaign_service.get_advertiser_campaigns(message.from_user.id)
        app_service = ApplicationService(session)

        text = "👥 Заявки на твои кампании:\n\n"
        has_applications = False

        for campaign in campaigns:
            applications = await app_service.get_campaign_applications(campaign.id)
            if applications:
                has_applications = True
                text += f"📌 Кампания '{campaign.title}' (ID {campaign.id}):\n"
                for app in applications:
                    status_text = {
                        "pending": "⏳ На рассмотрении",
                        "accepted": "✅ Принята",
                        "rejected": "❌ Отклонена",
                    }.get(app.status, app.status)
                    text += f"   - Блогер ID {app.influencer_id}: {status_text}\n"
                text += "\n"

        if has_applications:
            await message.answer(text)
        else:
            await message.answer("❌ Заявок пока нет.")
