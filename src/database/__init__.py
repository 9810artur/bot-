"""Database initialization with async support."""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool

from src.config.settings import settings


# Create async engine
engine = create_async_engine(
    settings.get_database_url(),
    echo=settings.DEBUG,
    future=True,
    poolclass=NullPool,
)

# Create async session factory
async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db_session() -> AsyncSession:
    """Get database session."""
    async with async_session_factory() as session:
        yield session
