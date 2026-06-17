"""Shared test constants."""

TEST_SECRET = 'dGVzdC1zZWNyZXQ='
TEST_HMAC_ALG = 'SHA256'
TEST_LOG_LEVEL = 'info'
TEST_HOST = '127.0.0.1'
TEST_PORT = 8080
TEST_LISTEN = f'{TEST_HOST}:{TEST_PORT}'
TEST_MAX_MSG_SIZE = 1_048_576
INVALID_SECRET = '!!!invalid-base64!!!'
INVALID_LOG_LEVEL = 'invalid'

MSG_HELLO = 'hello'
MSG_HELLO_MODIFIED = 'hello!'
MSG_TEST = 'test message'
MSG_DETERMINISTIC = 'deterministic test'
MSG_UNICODE = 'Привет, мир! 👋'
MSG_EMPTY = ''

INVALID_SIGNATURE_FORMAT = '@@@invalid@@@'
VALID_SIGNATURE_EXAMPLE = 'dGVzdA'

NEW_MAX_MSG_SIZE = 100

# HMAC service test constants
TEST_KEY = b'test-secret-key-12345678'
TEST_KEY_1 = b'key1'
TEST_KEY_2 = b'key2'
SHORT_SIGNATURE = b'short'
LONG_SIGNATURE = b'x' * 100
SHA256_DIGEST_SIZE = 32
