"""Module with HMAC sign functions."""

import hashlib
import hmac


class HMACSigner:
    """Class for HMAC sign and verify signature."""

    def __init__(self, key: bytes):
        self.key = key

    def sign(self, msg: str) -> bytes:
        msg_bytes = msg.encode('utf-8')
        return hmac.new(self.key, msg_bytes, hashlib.sha256).digest()

    def verify(self, msg: str, signature: bytes) -> bool:
        expected_sig = self.sign(msg)
        return hmac.compare_digest(expected_sig, signature)
