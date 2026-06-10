"""
Engine -> Session Factory -> Dependency
"""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import get_settings

settings = get_settings()
kwargs = {
    "url": settings.DB_URL,
    "pool_pre_ping": True,
    "echo": False,  # default logging disabled
}
engine = create_async_engine(**kwargs)

SessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    1. `with` is just some fancy try-finally, it handles .open() and .close() itself
    2. `yield` returns a generator object (which is just fancy iterator), but yield is something which creates the boundary b/w open and close
    3. Basically `yield` is something which divides the function in two parts (before yield and after yield)
    4. Creates one SQLalchemy session per request.
    """
    async with SessionLocal() as session:
        yield session
