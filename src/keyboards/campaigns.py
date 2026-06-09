"""Campaign action keyboards."""

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_campaigns_list_keyboard(page: int = 0) -> InlineKeyboardMarkup:
    """Get campaigns list navigation keyboard."""
    buttons = []
    if page > 0:
        buttons.append(
            InlineKeyboardButton(text="⬅️ Предыдущая", callback_data=f"campaigns_page_{page - 1}")
        )
    buttons.append(
        InlineKeyboardButton(text="➕ Новая кампания", callback_data="create_campaign")
    )
    buttons.append(
        InlineKeyboardButton(text="➡️ Следующая", callback_data=f"campaigns_page_{page + 1}")
    )

    return InlineKeyboardMarkup(
        inline_keyboard=[buttons]
    )


def get_campaign_details_keyboard(campaign_id: int) -> InlineKeyboardMarkup:
    """Get campaign details keyboard with apply button."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📝 Подать заявку",
                    callback_data=f"apply_campaign_{campaign_id}",
                ),
            ],
            [
                InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_campaigns"),
            ],
        ]
    )


def get_campaign_management_keyboard(campaign_id: int) -> InlineKeyboardMarkup:
    """Get campaign management keyboard for advertiser."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="👥 Заявки",
                    callback_data=f"campaign_applications_{campaign_id}",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="✏️ Редактировать",
                    callback_data=f"edit_campaign_{campaign_id}",
                ),
                InlineKeyboardButton(
                    text="🗑️ Удалить",
                    callback_data=f"delete_campaign_{campaign_id}",
                ),
            ],
            [
                InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_my_campaigns"),
            ],
        ]
    )


def get_application_action_keyboard(application_id: int) -> InlineKeyboardMarkup:
    """Get application action keyboard for advertiser."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Принять",
                    callback_data=f"accept_application_{application_id}",
                ),
                InlineKeyboardButton(
                    text="❌ Отклонить",
                    callback_data=f"reject_application_{application_id}",
                ),
            ],
        ]
    )
