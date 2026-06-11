"""Tests for codec module."""

import pytest

from src.codec import decode, encode


def test_encode_decode_cycle():
    """Test encoding and decoding cycle."""
    original_data = b'Hello, World!'
    encoded = encode(original_data)
    decoded = decode(encoded)
    assert decoded == original_data


def test_encode_no_padding():
    """Test that encoded string has no padding characters."""
    data = b'test data for encoding'
    encoded = encode(data)
    assert '=' not in encoded


def test_encode_empty_bytes():
    """Test encoding empty bytes."""
    encoded = encode(b'')
    decoded = decode(encoded)
    assert decoded == b''


def test_decode_empty_string():
    """Test decoding empty string returns empty bytes."""
    assert decode('') == b''


def test_decode_invalid_characters():
    """Test decoding string with invalid characters."""
    invalid_strings = ['@@@', 'hello!', 'with space']
    for s in invalid_strings:
        with pytest.raises(ValueError):
            decode(s)


def test_deterministic_encoding():
    """Test that encoding is deterministic."""
    data = b'test deterministic'
    encoded1 = encode(data)
    encoded2 = encode(data)
    assert encoded1 == encoded2


def test_decode_valid_base64url():
    """Test decoding valid base64url strings."""
    encoded = 'dGVzdA'
    decoded = decode(encoded)
    assert decoded == b'test'
