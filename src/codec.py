"""Module with codec functions."""

import base64


def encode(data: bytes) -> str:
    """Encode bytes to base64url string without padding."""
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('ascii')


def decode(data: str) -> bytes:
    """Decode base64url string to bytes."""
    if not data:
        return b''
    try:
        return base64.b64decode(
            data + '=' * (4 - len(data) % 4),
            altchars=b'-_',
            validate=True,
        )
    except Exception:
        raise ValueError('Invalid base64url string')
