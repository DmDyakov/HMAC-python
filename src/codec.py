"""Module with codec functions."""

import base64

from src.constants import BASE64_BLOCK_SIZE


def encode(data: bytes) -> str:
    """Encode bytes to base64url string without padding."""
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('ascii')


def decode(data: str) -> bytes:
    """Decode base64url string to bytes."""
    if not data:
        return b''
    try:
        padding_length = (
            BASE64_BLOCK_SIZE - len(data) % BASE64_BLOCK_SIZE
        ) % BASE64_BLOCK_SIZE
        return base64.b64decode(
            data + '=' * padding_length,
            altchars=b'-_',
            validate=True,
        )
    except Exception:
        raise ValueError('Invalid base64url string')
