"""Utility validators."""

from datetime import datetime


def validate_date(date_string: str) -> tuple[bool, datetime | None]:
    """Validate date string.

    Args:
        date_string: Date string in format YYYY-MM-DD HH:MM

    Returns:
        Tuple of (is_valid, datetime_object)
    """
    try:
        dt = datetime.strptime(date_string, "%Y-%m-%d %H:%M")
        return True, dt
    except ValueError:
        return False, None


def validate_price(price_string: str) -> tuple[bool, float | None]:
    """Validate price string.

    Args:
        price_string: Price as string

    Returns:
        Tuple of (is_valid, price_float)
    """
    try:
        price = float(price_string)
        if price < 0:
            return False, None
        return True, price
    except ValueError:
        return False, None


def validate_followers(followers_string: str) -> tuple[bool, int | None]:
    """Validate followers count string.

    Args:
        followers_string: Followers count as string

    Returns:
        Tuple of (is_valid, count_int)
    """
    try:
        count = int(followers_string)
        if count < 0:
            return False, None
        return True, count
    except ValueError:
        return False, None
