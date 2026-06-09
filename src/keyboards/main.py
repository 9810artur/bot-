"""Main keyboard builders."""

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton


def get_main_menu_keyboard() -> ReplyKeyboardMarkup:
    """Get main menu keyboard."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📊 Мой профиль")],
            [KeyboardButton(text="⚙️ Настройки")],
            [KeyboardButton(text="❓ Помощь")],
        ],
        resize_keyboard=True,
        one_time_keyboard=False,
    )


def get_role_selection_keyboard() -> InlineKeyboardMarkup:
    """Get role selection keyboard."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💼 Бизнес",
                    callback_data="role_advertiser",
                ),
                InlineKeyboardButton(
                    text="📱 Блогер",
                    callback_data="role_influencer",
                ),
            ],
        ]
    )


def get_influencer_menu_keyboard() -> ReplyKeyboardMarkup:
    """Get influencer menu keyboard."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👤 Моя анкета")],
            [KeyboardButton(text="📢 Просмотр кампаний")],
            [KeyboardButton(text="📋 Мои заявки")],
            [KeyboardButton(text="⚙️ Настройки")],
        ],
        resize_keyboard=True,
        one_time_keyboard=False,
    )


def get_advertiser_menu_keyboard() -> ReplyKeyboardMarkup:
    """Get advertiser menu keyboard."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ Создать кампанию")],
            [KeyboardButton(text="📊 Мои кампании")],
            [KeyboardButton(text="👥 Заявки")],
            [KeyboardButton(text="⚙️ Настройки")],
        ],
        resize_keyboard=True,
        one_time_keyboard=False,
    )


def get_confirm_keyboard() -> InlineKeyboardMarkup:
    """Get confirm/cancel keyboard."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm"),
                InlineKeyboardButton(text="❌ Отмена", callback_data="cancel"),
            ],
        ]
    )


def get_skip_keyboard() -> InlineKeyboardMarkup:
    """Get skip keyboard."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="⏭️ Пропустить", callback_data="skip"),
            ],
        ]
    )
