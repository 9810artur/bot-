"""Decorators for handlers."""

import logging
from functools import wraps
from typing import Callable, Any

logger = logging.getLogger(__name__)


def handle_errors(func: Callable) -> Callable:
    """Decorator for handling errors in handlers."""

    @wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}", exc_info=True)
            # Try to send error message to user
            message = args[1] if len(args) > 1 else kwargs.get("message")
            if message:
                await message.answer(
                    "❌ Ошибка при обработке. Попробуйте позже."
                )

    return wrapper


def require_registered(func: Callable) -> Callable:
    """Decorator for requiring user to be registered."""

    @wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        from src.services.user_service import UserService
        from src.database import async_session_factory

        message = args[1] if len(args) > 1 else kwargs.get("message")
        if not message:
            return

        async with async_session_factory() as session:
            user_service = UserService(session)
            user = await user_service.get_user(message.from_user.id)

        if not user:
            await message.answer(
                "❌ Вы не регистрированы.\n"
                "/start - Начните регистрацию"
            )
            return

        return await func(*args, **kwargs)

    return wrapper
