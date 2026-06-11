"""Utility for rotating secret key"""

import base64
import json
import os
import sys


def generate_secret(length: int = 32) -> str:
    """
    Generate new random secret key.

    :param length: Key length in bytes.
    :return: Base64url encoded key without padding.
    """
    import secrets

    key = secrets.token_bytes(length)
    return base64.urlsafe_b64encode(key).rstrip(b'=').decode('ascii')


def rotate_secret(config_path: str = 'config.json'):
    """
    Rotate secret key in config file.

    :param config_path: Path to configuration file.
    """
    if not os.path.exists(config_path):
        print(f"Error: Config file '{config_path}' not found", file=sys.stderr)
        sys.exit(1)

    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    old_secret = config.get('secret', 'none')
    new_secret = generate_secret()
    config['secret'] = new_secret

    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)
        f.write('\n')

    print('Secret rotated successfully!')
    print(f'Old secret: {old_secret}')
    print(f'New secret: {new_secret}')
    print(f'Config file updated: {config_path}')


if __name__ == '__main__':
    rotate_secret()
