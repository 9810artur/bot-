"""Bot configuration and constants."""

from src.config.settings import settings


class BotConfig:
    """Bot configuration class."""

    TOKEN = settings.BOT_TOKEN
    DEBUG = settings.DEBUG
    ADMIN_IDS = settings.admin_ids_list
    APP_NAME = settings.APP_NAME


class BotConstants:
    """Bot constants."""

    # Timeouts
    HANDLER_TIMEOUT = 30  # seconds
    POLLING_TIMEOUT = 30  # seconds

    # Message limits
    MAX_MESSAGE_LENGTH = 4096
    MAX_CAPTION_LENGTH = 1024

    # Pagination
    ITEMS_PER_PAGE = 10

    # Cooldowns
    COMMAND_COOLDOWN = 2  # seconds
