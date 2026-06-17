"""Tests for FastAPI router."""

from fastapi.testclient import TestClient

from tests.constants import (
    INVALID_SIGNATURE_FORMAT,
    MSG_DETERMINISTIC,
    MSG_EMPTY,
    MSG_HELLO,
    MSG_HELLO_MODIFIED,
    MSG_TEST,
    MSG_UNICODE,
    TEST_MAX_MSG_SIZE,
    VALID_SIGNATURE_EXAMPLE,
)


def test_sign_success(client: TestClient):
    response = client.post('/sign', json={'msg': MSG_HELLO})
    assert response.status_code == 200
    data = response.json()
    assert 'signature' in data
    assert len(data['signature']) > 0


def test_sign_empty_message(client: TestClient):
    response = client.post('/sign', json={'msg': MSG_EMPTY})
    assert response.status_code == 422


def test_sign_missing_msg(client: TestClient):
    response = client.post('/sign', json={})
    assert response.status_code == 422


def test_verify_success(client: TestClient):
    sign_response = client.post('/sign', json={'msg': MSG_TEST})
    assert sign_response.status_code == 200
    signature = sign_response.json()['signature']

    verify_response = client.post(
        '/verify',
        json={'msg': MSG_TEST, 'signature': signature},
    )
    assert verify_response.status_code == 200
    assert verify_response.json()['ok'] is True


def test_verify_modified_message(client: TestClient):
    sign_response = client.post('/sign', json={'msg': MSG_HELLO})
    signature = sign_response.json()['signature']

    verify_response = client.post(
        '/verify',
        json={'msg': MSG_HELLO_MODIFIED, 'signature': signature},
    )
    assert verify_response.status_code == 200
    assert verify_response.json()['ok'] is False


def test_verify_invalid_signature(client: TestClient):
    sign_response = client.post('/sign', json={'msg': MSG_HELLO})
    signature = sign_response.json()['signature']

    modified_sig = signature[:-1] + ('A' if signature[-1] != 'A' else 'B')

    verify_response = client.post(
        '/verify',
        json={'msg': MSG_HELLO, 'signature': modified_sig},
    )
    assert verify_response.status_code == 200
    assert verify_response.json()['ok'] is False


def test_verify_invalid_signature_format(client: TestClient):
    response = client.post(
        '/verify',
        json={'msg': MSG_HELLO, 'signature': INVALID_SIGNATURE_FORMAT},
    )
    assert response.status_code == 400
    assert response.json()['detail'] == 'invalid_signature_format'


def test_verify_empty_message(client: TestClient):
    response = client.post(
        '/verify',
        json={'msg': MSG_EMPTY, 'signature': VALID_SIGNATURE_EXAMPLE},
    )
    assert response.status_code == 422


def test_verify_missing_fields(client: TestClient):
    response = client.post('/verify', json={})
    assert response.status_code == 422


def test_large_message(client: TestClient):
    large_msg = 'x' * (TEST_MAX_MSG_SIZE + 1)
    response = client.post('/sign', json={'msg': large_msg})
    assert response.status_code == 413


def test_deterministic_signature(client: TestClient):
    response1 = client.post('/sign', json={'msg': MSG_DETERMINISTIC})
    response2 = client.post('/sign', json={'msg': MSG_DETERMINISTIC})

    sig1 = response1.json()['signature']
    sig2 = response2.json()['signature']

    assert sig1 == sig2


def test_unicode_message(client: TestClient):
    sign_response = client.post('/sign', json={'msg': MSG_UNICODE})
    assert sign_response.status_code == 200
    signature = sign_response.json()['signature']

    verify_response = client.post(
        '/verify',
        json={'msg': MSG_UNICODE, 'signature': signature},
    )
    assert verify_response.status_code == 200
    assert verify_response.json()['ok'] is True
