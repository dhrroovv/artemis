from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from app.core.config import get_settings
from app.core.logger import get_logger, setup_logging
from app.db.session import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Here we can define the events we need to initialise/start before the application startups \
    and ends gracefully after the application shutdown. The boundary is 'yield'.
    """
    # Config
    settings = get_settings()

    # Logger
    setup_logging(settings.LOG_LEVEL)
    logger = get_logger(__name__)

    # DB Liveness check
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
    except Exception:
        logger.error("Database connectivity check failed")
        raise

    logger.info("Application starting...")
    try:
        yield
    finally:
        await engine.dispose()
        logger.info("Application shutting down...")


app = FastAPI(lifespan=lifespan)
