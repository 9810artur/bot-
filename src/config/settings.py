"""Application settings and configuration."""

from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Bot Configuration
    BOT_TOKEN: str = Field(..., description="Telegram Bot Token")
    DEBUG: bool = Field(default=False, description="Debug mode")

    # Database Configuration
    DB_HOST: str = Field(default="localhost", description="Database host")
    DB_PORT: int = Field(default=5432, description="Database port")
    DB_NAME: str = Field(default="localsbot", description="Database name")
    DB_USER: str = Field(default="postgres", description="Database user")
    DB_PASSWORD: str = Field(default="postgres", description="Database password")
    DATABASE_URL: Optional[str] = Field(
        default=None, description="Database URL for SQLAlchemy"
    )

    # Redis Configuration
    REDIS_HOST: str = Field(default="localhost", description="Redis host")
    REDIS_PORT: int = Field(default=6379, description="Redis port")
    REDIS_DB: int = Field(default=0, description="Redis database number")

    # Application Settings
    APP_NAME: str = Field(default="LocalAdsBot", description="Application name")
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    TIMEZONE: str = Field(default="UTC", description="Application timezone")

    # Admin Configuration
    ADMIN_IDS: str = Field(default="", description="Comma-separated admin IDs")

    class Config:
        """Pydantic config."""

        env_file = ".env"
        case_sensitive = True

    @property
    def admin_ids_list(self) -> list[int]:
        """Get admin IDs as list of integers."""
        if not self.ADMIN_IDS:
            return []
        return [int(admin_id) for admin_id in self.ADMIN_IDS.split(",")]

    def get_database_url(self) -> str:
        """Get database URL for SQLAlchemy."""
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


settings = Settings()  # type: ignore
