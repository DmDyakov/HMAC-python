"""Tests for config module."""

import json
import os
import tempfile

import pytest

from src.config import Settings, get_settings
from tests.constants import (
    INVALID_LOG_LEVEL,
    INVALID_SECRET,
    NEW_MAX_MSG_SIZE,
    TEST_HMAC_ALG,
    TEST_HOST,
    TEST_LISTEN,
    TEST_LOG_LEVEL,
    TEST_MAX_MSG_SIZE,
    TEST_PORT,
    TEST_SECRET,
)


def test_load_valid_config():
    config_data = {
        'hmac_alg': TEST_HMAC_ALG,
        'secret': TEST_SECRET,
        'log_level': TEST_LOG_LEVEL,
        'listen': TEST_LISTEN,
        'max_msg_size_bytes': TEST_MAX_MSG_SIZE,
    }

    with tempfile.NamedTemporaryFile(
        mode='w', suffix='.json', delete=False
    ) as f:
        json.dump(config_data, f)
        config_path = f.name

    try:
        settings = get_settings(config_path)
        assert settings.hmac_alg == TEST_HMAC_ALG
        assert settings.log_level == TEST_LOG_LEVEL
        assert settings.host == TEST_HOST
        assert settings.port == TEST_PORT
        assert settings.max_msg_size_bytes == TEST_MAX_MSG_SIZE
    finally:
        os.unlink(config_path)


def test_load_config_missing_secret():
    config_data = {
        'hmac_alg': TEST_HMAC_ALG,
        'log_level': TEST_LOG_LEVEL,
        'listen': TEST_LISTEN,
        'max_msg_size_bytes': TEST_MAX_MSG_SIZE,
    }

    with tempfile.NamedTemporaryFile(
        mode='w', suffix='.json', delete=False
    ) as f:
        json.dump(config_data, f)
        config_path = f.name

    try:
        with pytest.raises(ValueError):
            get_settings(config_path)
    finally:
        os.unlink(config_path)


def test_load_config_invalid_secret():
    config_data = {
        'hmac_alg': TEST_HMAC_ALG,
        'secret': INVALID_SECRET,
        'log_level': TEST_LOG_LEVEL,
        'listen': TEST_LISTEN,
        'max_msg_size_bytes': TEST_MAX_MSG_SIZE,
    }

    with tempfile.NamedTemporaryFile(
        mode='w', suffix='.json', delete=False
    ) as f:
        json.dump(config_data, f)
        config_path = f.name

    try:
        with pytest.raises(ValueError):
            get_settings(config_path)
    finally:
        os.unlink(config_path)


def test_load_config_invalid_log_level():
    config_data = {
        'hmac_alg': TEST_HMAC_ALG,
        'secret': TEST_SECRET,
        'log_level': INVALID_LOG_LEVEL,
        'listen': TEST_LISTEN,
        'max_msg_size_bytes': TEST_MAX_MSG_SIZE,
    }

    with tempfile.NamedTemporaryFile(
        mode='w', suffix='.json', delete=False
    ) as f:
        json.dump(config_data, f)
        config_path = f.name

    try:
        with pytest.raises(ValueError):
            get_settings(config_path)
    finally:
        os.unlink(config_path)


def test_settings_is_frozen():
    settings = Settings(secret=TEST_SECRET)
    with pytest.raises(Exception):
        settings.max_msg_size_bytes = NEW_MAX_MSG_SIZE
