"""Entry point for LocalAdsBot application."""

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from src.config.settings import settings
from src.config.logging_config import setup_logging


async def main() -> None:
    """Main function to start the bot."""
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting LocalAdsBot...")

    # Initialize bot and dispatcher
    bot = Bot(token=settings.BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # TODO: Register handlers, middlewares, routers

    try:
        logger.info("Bot started successfully")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Error starting bot: {e}", exc_info=True)
    finally:
        await bot.session.close()
        logger.info("Bot stopped")


if __name__ == "__main__":
    asyncio.run(main())
