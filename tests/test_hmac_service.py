"""Tests for HMAC service module."""

from src.hmac_service import HMACSigner
from tests.constants import (
    LONG_SIGNATURE,
    MSG_EMPTY,
    MSG_HELLO,
    MSG_HELLO_MODIFIED,
    MSG_TEST,
    SHA256_DIGEST_SIZE,
    SHORT_SIGNATURE,
    TEST_KEY,
    TEST_KEY_1,
    TEST_KEY_2,
)


def get_signer() -> HMACSigner:
    """Helper to create signer with test key."""
    return HMACSigner(TEST_KEY)


def test_sign_returns_bytes():
    """Test that sign returns bytes."""
    signer = get_signer()
    signature = signer.sign(MSG_HELLO)
    assert isinstance(signature, bytes)
    assert len(signature) == SHA256_DIGEST_SIZE


def test_sign_deterministic():
    """Test that signing is deterministic."""
    signer = get_signer()
    sig1 = signer.sign(MSG_HELLO)
    sig2 = signer.sign(MSG_HELLO)
    assert sig1 == sig2


def test_verify_valid_signature():
    """Test verification of valid signature."""
    signer = get_signer()
    msg = MSG_TEST
    sig = signer.sign(msg)
    assert signer.verify(msg, sig) is True


def test_verify_invalid_message():
    """Test verification fails with different message."""
    signer = get_signer()
    sig = signer.sign(MSG_HELLO)
    assert signer.verify(MSG_HELLO_MODIFIED, sig) is False


def test_verify_invalid_signature():
    """Test verification fails with modified signature."""
    signer = get_signer()
    msg = MSG_HELLO
    sig = signer.sign(msg)

    modified_sig = bytearray(sig)
    modified_sig[0] ^= 1

    assert signer.verify(msg, bytes(modified_sig)) is False


def test_verify_wrong_length_signature():
    """Test verification with wrong length signature."""
    signer = get_signer()
    msg = MSG_HELLO
    assert signer.verify(msg, SHORT_SIGNATURE) is False
    assert signer.verify(msg, LONG_SIGNATURE) is False


def test_different_keys_produce_different_signatures():
    """Test that different keys produce different signatures."""
    signer1 = HMACSigner(TEST_KEY_1)
    signer2 = HMACSigner(TEST_KEY_2)

    sig1 = signer1.sign(MSG_HELLO)
    sig2 = signer2.sign(MSG_HELLO)

    assert sig1 != sig2


def test_empty_message():
    """Test signing and verifying empty message."""
    signer = get_signer()
    sig = signer.sign(MSG_EMPTY)
    assert isinstance(sig, bytes)
    assert len(sig) == SHA256_DIGEST_SIZE
    assert signer.verify(MSG_EMPTY, sig) is True
