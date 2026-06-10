from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import get_settings
from app.core.logger import get_logger, setup_logging


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

    logger.info("Application starting...")
    try:
        yield
    finally:
        logger.info("Application shutting down...")


app = FastAPI(lifespan=lifespan)
