"""Settings and help command handlers."""

import logging
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.user_service import UserService
from src.keyboards import get_main_menu_keyboard
from src.database import async_session_factory

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command("help"))
async def help_command(message: Message) -> None:
    """Show help message."""
    help_text = (
        "📚 Справка по командам LocalAdsBot\n\n"
        "/start - Начать работу\n"
        "/influencer - Меню блогера\n"
        "/advertiser - Меню бизнеса\n"
        "/profile - Мой профиль\n"
        "/help - Эта справка\n\n"
        "📋 Функции:\n\n"
        "🎯 Для блогеров:\n"
        "• Создайте свою анкету с информацией о вас\n"
        "• Просматривайте доступные кампании\n"
        "• Подавайте заявки на участие\n\n"
        "💼 Для бизнеса:\n"
        "• Создавайте рекламные кампании\n"
        "• Просматривайте заявки от блогеров\n"
        "• Принимайте или отклоняйте предложения"
    )
    await message.answer(help_text)


@router.message(Command("profile"))
async def my_profile(message: Message) -> None:
    """Show user profile."""
    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(message.from_user.id)

    if not user:
        await message.answer(
            "❌ Вы не зарегистрированы.\n"
            "Используйте /start для регистрации."
        )
        return

    role_text = {
        "advertiser": "💼 Бизнес",
        "influencer": "📱 Блогер",
        "admin": "👨‍💼 Администратор",
    }.get(user.role, user.role)

    profile_text = (
        f"👤 Ваш профиль\n\n"
        f"Имя: {user.full_name}\n"
        f"Username: @{user.username or 'Не указан'}\n"
        f"Город: {user.city or 'Не указан'}\n"
        f"Роль: {role_text}\n"
        f"Регистрация: {user.created_at.strftime('%d.%m.%Y %H:%M')}"
    )

    await message.answer(
        profile_text,
        reply_markup=get_main_menu_keyboard(),
    )


@router.message(Command("settings"))
async def settings_command(message: Message) -> None:
    """Show settings menu."""
    settings_text = (
        "⚙️ Настройки\n\n"
        "В разработке...\n\n"
        "Доступные опции:\n"
        "• Изменить профиль\n"
        "• Уведомления\n"
        "• Приватность"
    )
    await message.answer(settings_text)


@router.message(Command("admin"))
async def admin_command(message: Message) -> None:
    """Admin command (available only for admins)."""
    from src.config.settings import settings

    if message.from_user.id not in settings.admin_ids_list:
        await message.answer("❌ У вас нет прав для выполнения этой команды.")
        return

    admin_text = (
        "👨‍💼 Администраторский панель\n\n"
        "В разработке...\n\n"
        "Доступные функции:\n"
        "• Статистика\n"
        "• Управление пользователями\n"
        "• Управление кампаниями"
    )
    await message.answer(admin_text)
