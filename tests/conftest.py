"""Shared fixtures for tests."""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.config import Settings
from src.hmac_service import HMACSigner
from src.router import router


@pytest.fixture
def client() -> TestClient:
    """Create test client with fake secret key."""
    settings = Settings(secret='dGVzdC1zZWNyZXQ=')
    signer = HMACSigner(settings.secret_bytes)

    app = FastAPI()
    app.state.settings = settings
    app.state.signer = signer
    app.include_router(router)

    return TestClient(app)
