"""Tests for HMAC service module."""

from src.hmac_service import HMACSigner


def get_signer() -> HMACSigner:
    """Helper to create signer with test key."""
    return HMACSigner(b'test-secret-key-12345678')


def test_sign_returns_bytes():
    """Test that sign returns bytes."""
    signer = get_signer()
    signature = signer.sign('hello')
    assert isinstance(signature, bytes)
    assert len(signature) == 32


def test_sign_deterministic():
    """Test that signing is deterministic."""
    signer = get_signer()
    sig1 = signer.sign('hello')
    sig2 = signer.sign('hello')
    assert sig1 == sig2


def test_verify_valid_signature():
    """Test verification of valid signature."""
    signer = get_signer()
    msg = 'test message'
    sig = signer.sign(msg)
    assert signer.verify(msg, sig) is True


def test_verify_invalid_message():
    """Test verification fails with different message."""
    signer = get_signer()
    sig = signer.sign('hello')
    assert signer.verify('hello!', sig) is False


def test_verify_invalid_signature():
    """Test verification fails with modified signature."""
    signer = get_signer()
    msg = 'hello'
    sig = signer.sign(msg)

    modified_sig = bytearray(sig)
    modified_sig[0] ^= 1

    assert signer.verify(msg, bytes(modified_sig)) is False


def test_verify_wrong_length_signature():
    """Test verification with wrong length signature."""
    signer = get_signer()
    msg = 'hello'
    assert signer.verify(msg, b'short') is False
    assert signer.verify(msg, b'x' * 100) is False


def test_different_keys_produce_different_signatures():
    """Test that different keys produce different signatures."""
    signer1 = HMACSigner(b'key1')
    signer2 = HMACSigner(b'key2')

    sig1 = signer1.sign('hello')
    sig2 = signer2.sign('hello')

    assert sig1 != sig2


def test_empty_message():
    """Test signing and verifying empty message."""
    signer = get_signer()
    sig = signer.sign('')
    assert isinstance(sig, bytes)
    assert len(sig) == 32
    assert signer.verify('', sig) is True
