"""Module with FastAPI application"""

from fastapi import FastAPI

from src.config import get_settings
from src.hmac_service import HMACSigner
from src.logger import setup_logging
from src.router import router


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    settings = get_settings()
    setup_logging(settings.log_level)

    signer = HMACSigner(settings.secret_bytes)

    app = FastAPI()
    app.state.settings = settings
    app.state.signer = signer
    app.include_router(router)

    return app


app = create_app()
