"""Application configuration loaded from config.json."""

import base64
import json
from functools import lru_cache
from typing import Literal

from pydantic import BaseModel, Field, field_validator

from src.constants import BASE64_BLOCK_SIZE, MAX_PORT, MIN_PORT


class Settings(BaseModel):
    """App settings."""

    model_config = {'frozen': True}

    secret: str
    hmac_alg: Literal['SHA256'] = 'SHA256'
    log_level: Literal['debug', 'info', 'warning', 'error', 'critical'] = (
        'info'
    )
    listen: str = '127.0.0.1:8080'
    max_msg_size_bytes: int = Field(default=1_048_576, gt=0)

    @property
    def host(self) -> str:
        return self.listen.split(':')[0]

    @property
    def port(self) -> int:
        return int(self.listen.split(':')[1])

    @property
    def secret_bytes(self) -> bytes:
        padding = BASE64_BLOCK_SIZE - len(self.secret) % BASE64_BLOCK_SIZE
        secret_padded = self.secret
        if padding != BASE64_BLOCK_SIZE:
            secret_padded += '=' * padding
        return base64.urlsafe_b64decode(secret_padded)

    @field_validator('listen')
    @classmethod
    def validate_listen(cls, v: str) -> str:
        if ':' not in v:
            raise ValueError('Listen must be in format "host:port"')
        _, port = v.split(':')
        if not MIN_PORT <= int(port) <= MAX_PORT:
            raise ValueError(f'Port must be between {MIN_PORT} and {MAX_PORT}')
        return v

    @field_validator('secret')
    @classmethod
    def validate_secret(cls, v: str) -> str:
        if not v:
            raise ValueError('Secret cannot be empty')
        try:
            padding = BASE64_BLOCK_SIZE - len(v) % BASE64_BLOCK_SIZE
            v_padded = v + '=' * padding if padding != BASE64_BLOCK_SIZE else v
            base64.urlsafe_b64decode(v_padded)
        except Exception:
            raise ValueError('Secret must be valid base64url')
        return v


@lru_cache()
def get_settings(path: str = 'config.json') -> Settings:
    """Загружает настройки из JSON-файла."""
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    return Settings(**data)
