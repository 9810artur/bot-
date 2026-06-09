"""Constants for LocalAdsBot."""

from enum import Enum


class PaginationConstants:
    """Pagination constants."""

    ITEMS_PER_PAGE = 5
    MAX_ITEMS_PER_PAGE = 10


class MessageConstants:
    """Message constants."""

    # Registration
    WELCOME_MESSAGE = (
        "👋 Привет! Добро пожаловать в LocalAdsBot!\n\n"
        "Маркетплейс рекламы между бизнесом и блогерами."
    )

    REGISTRATION_COMPLETE = (
        "✅ Регистрация завершена!"
    )

    # Errors
    USER_NOT_FOUND = "❌ Пользователь не найден."
    CAMPAIGN_NOT_FOUND = "❌ Кампания не найдена."
    APPLICATION_NOT_FOUND = "❌ Заявка не найдена."
    PROFILE_NOT_FOUND = "❌ Анкета не найдена."
    ERROR = "❌ Ошибка при обработке запроса."


class ValidationConstants:
    """Validation constants."""

    MIN_USERNAME_LENGTH = 3
    MAX_USERNAME_LENGTH = 32
    MIN_CAMPAIGN_TITLE_LENGTH = 5
    MAX_CAMPAIGN_TITLE_LENGTH = 255
    MIN_PRICE = 0.0
    MAX_PRICE = 1000000.0
    MIN_FOLLOWERS = 0
    MAX_FOLLOWERS = 100000000
