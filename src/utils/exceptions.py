"""Exception classes for LocalAdsBot."""


class LocalAdsBotException(Exception):
    """Base exception for LocalAdsBot."""

    pass


class UserNotFound(LocalAdsBotException):
    """User not found exception."""

    pass


class CampaignNotFound(LocalAdsBotException):
    """Campaign not found exception."""

    pass


class ApplicationNotFound(LocalAdsBotException):
    """Application not found exception."""

    pass


class ProfileNotFound(LocalAdsBotException):
    """Profile not found exception."""

    pass


class InvalidRoleError(LocalAdsBotException):
    """Invalid role error."""

    pass


class DuplicateApplicationError(LocalAdsBotException):
    """Application already exists error."""

    pass


class InvalidStatusError(LocalAdsBotException):
    """Invalid status error."""

    pass
