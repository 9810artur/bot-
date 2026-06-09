"""Logging middleware."""

import logging
from typing import Any, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import Update

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseMiddleware):
    """Middleware for logging all updates."""

    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Any],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
        """Log update and pass to handler."""
        if event.message:
            logger.info(
                f"Message from {event.message.from_user.id}: {event.message.text}"
            )
        elif event.callback_query:
            logger.info(
                f"Callback from {event.callback_query.from_user.id}: "
                f"{event.callback_query.data}"
            )

        return await handler(event, data)
