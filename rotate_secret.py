"""Utility for rotating secret key"""

import base64
import json
import logging
import os
import sys

DEFAULT_KEY_LENGTH = 32
DEFAULT_CONFIG_PATH = 'config.json'

logger = logging.getLogger(__name__)


def generate_secret(length: int = DEFAULT_KEY_LENGTH) -> str:
    """
    Generate new random secret key.

    :param length: Key length in bytes.
    :return: Base64url encoded key without padding.
    """
    import secrets

    key = secrets.token_bytes(length)
    return base64.urlsafe_b64encode(key).rstrip(b'=').decode('ascii')


def rotate_secret(config_path: str = DEFAULT_CONFIG_PATH):
    """
    Rotate secret key in config file.

    :param config_path: Path to configuration file.
    """
    if not os.path.exists(config_path):
        logger.error("Config file '%s' not found", config_path)
        sys.exit(1)

    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    old_secret = config.get('secret', 'none')
    new_secret = generate_secret()
    config['secret'] = new_secret

    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)
        f.write('\n')

    logger.info('Secret rotated successfully!')
    logger.info('Old secret: %s', old_secret)
    logger.info('New secret: %s', new_secret)
    logger.info('Config file updated: %s', config_path)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )
    rotate_secret()
