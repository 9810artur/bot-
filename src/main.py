"""Entry point for LocalAdsBot application."""

import asyncio
import logging
import sys
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from src.config.settings import settings
from src.config.logging_config import setup_logging
from src.database import engine
from src.database.models import Base
from src.handlers import (
    registration_router,
    influencer_router,
    advertiser_router,
    callbacks_router,
    common_router,
)
from src.middlewares import LoggingMiddleware


async def create_tables() -> None:
    """Create database tables."""
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except Exception as e:
        raise Exception(f"Failed to create database tables: {e}")


async def main() -> None:
    """Main function to start the bot."""
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info(f"Starting {settings.APP_NAME}...")

    # Validate required settings
    if not settings.BOT_TOKEN or settings.BOT_TOKEN == "your_telegram_bot_token_here":
        logger.error("BOT_TOKEN is not configured. Please set it in .env file.")
        sys.exit(1)

    # Create database tables
    try:
        await create_tables()
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}", exc_info=True)
        sys.exit(1)

    # Initialize bot and dispatcher
    try:
        bot = Bot(token=settings.BOT_TOKEN)
        storage = MemoryStorage()
        dp = Dispatcher(storage=storage)

        # Register middlewares
        dp.message.middleware(LoggingMiddleware())
        dp.callback_query.middleware(LoggingMiddleware())

        # Register routers (order matters)
        dp.include_router(registration_router)
        dp.include_router(influencer_router)
        dp.include_router(advertiser_router)
        dp.include_router(callbacks_router)
        dp.include_router(common_router)

        logger.info(f"{settings.APP_NAME} started successfully")
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as e:
        logger.error(f"Error starting bot: {e}", exc_info=True)
    finally:
        await bot.session.close()
        await engine.dispose()
        logger.info(f"{settings.APP_NAME} stopped")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot was stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)
