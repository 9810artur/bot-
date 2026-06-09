"""Registration command handler."""

import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
from sqlalchemy.ext.asyncio import AsyncSession

from src.states.registration import RegistrationStates
from src.keyboards import get_role_selection_keyboard
from src.services.user_service import UserService
from src.database import async_session_factory

router = Router()
logger = logging.getLogger(__name__)


@router.message(CommandStart())
async def start(message: Message, state: FSMContext) -> None:
    """Handle /start command."""
    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.get_user(message.from_user.id)

    if user:
        await message.answer(
            f"Привет, {message.from_user.first_name}! 👋\n"
            "Добро пожаловать обратно в LocalAdsBot!"
        )
    else:
        await message.answer(
            f"Привет, {message.from_user.first_name}! 👋\n"
            "Добро пожаловать в LocalAdsBot - маркетплейс рекламы!\n\n"
            "Выбери, кто ты?"
        )
        await state.set_state(RegistrationStates.waiting_for_role)
        await message.answer(
            "Выбери свою роль:",
            reply_markup=get_role_selection_keyboard(),
        )


@router.callback_query(
    RegistrationStates.waiting_for_role, F.data.startswith("role_")
)
async def select_role(callback: CallbackQuery, state: FSMContext) -> None:
    """Handle role selection."""
    role = callback.data.split("_")[1]
    await state.update_data(role=role)
    await callback.answer()

    await state.set_state(RegistrationStates.waiting_for_full_name)
    await callback.message.answer(
        "Введи своё полное имя:"
    )


@router.message(RegistrationStates.waiting_for_full_name)
async def get_full_name(message: Message, state: FSMContext) -> None:
    """Handle full name input."""
    await state.update_data(full_name=message.text)
    await state.set_state(RegistrationStates.waiting_for_username)
    await message.answer(
        "Введи свой username (или отправь '-' для пропуска):"
    )


@router.message(RegistrationStates.waiting_for_username)
async def get_username(message: Message, state: FSMContext) -> None:
    """Handle username input."""
    username = None if message.text == "-" else message.text
    await state.update_data(username=username)
    await state.set_state(RegistrationStates.waiting_for_city)
    await message.answer(
        "Введи свой город (или отправь '-' для пропуска):"
    )


@router.message(RegistrationStates.waiting_for_city)
async def get_city(message: Message, state: FSMContext) -> None:
    """Handle city input and complete registration."""
    city = None if message.text == "-" else message.text
    data = await state.get_data()

    async with async_session_factory() as session:
        user_service = UserService(session)
        user = await user_service.register_user(
            telegram_id=message.from_user.id,
            full_name=data["full_name"],
            role=data["role"],
            username=data.get("username"),
            city=city,
        )

    if user:
        logger.info(f"User registered: {user.telegram_id} ({user.role})")
        await message.answer(
            f"✅ Регистрация завершена!\n"
            f"Роль: {'💼 Бизнес' if user.role == 'advertiser' else '📱 Блогер'}\n"
            f"Имя: {user.full_name}"
        )
        await state.clear()
    else:
        await message.answer("❌ Ошибка при регистрации. Попробуй снова.")
