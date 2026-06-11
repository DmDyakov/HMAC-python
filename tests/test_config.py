"""Tests for config module."""

import json
import os
import tempfile

import pytest

from src.config import Settings, get_settings


def test_load_valid_config():
    config_data = {
        'hmac_alg': 'SHA256',
        'secret': 'dGVzdC1zZWNyZXQ=',
        'log_level': 'info',
        'listen': '127.0.0.1:8080',
        'max_msg_size_bytes': 1048576,
    }

    with tempfile.NamedTemporaryFile(
        mode='w', suffix='.json', delete=False
    ) as f:
        json.dump(config_data, f)
        config_path = f.name

    try:
        settings = get_settings(config_path)
        assert settings.hmac_alg == 'SHA256'
        assert settings.log_level == 'info'
        assert settings.host == '127.0.0.1'
        assert settings.port == 8080
        assert settings.max_msg_size_bytes == 1048576
    finally:
        os.unlink(config_path)


def test_load_config_missing_secret():
    config_data = {
        'hmac_alg': 'SHA256',
        'log_level': 'info',
        'listen': '127.0.0.1:8080',
        'max_msg_size_bytes': 1048576,
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
        'hmac_alg': 'SHA256',
        'secret': '!!!invalid-base64!!!',
        'log_level': 'info',
        'listen': '127.0.0.1:8080',
        'max_msg_size_bytes': 1048576,
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
        'hmac_alg': 'SHA256',
        'secret': 'dGVzdC1zZWNyZXQ=',
        'log_level': 'invalid',
        'listen': '127.0.0.1:8080',
        'max_msg_size_bytes': 1048576,
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
    settings = Settings(secret='dGVzdC1zZWNyZXQ=')
    with pytest.raises(Exception):
        settings.max_msg_size_bytes = 100
