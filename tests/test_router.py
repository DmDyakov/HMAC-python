"""Tests for FastAPI router."""

from fastapi.testclient import TestClient


def test_sign_success(client: TestClient):
    response = client.post('/sign', json={'msg': 'hello'})
    assert response.status_code == 200
    data = response.json()
    assert 'signature' in data
    assert len(data['signature']) > 0


def test_sign_empty_message(client: TestClient):
    response = client.post('/sign', json={'msg': ''})
    assert response.status_code == 422


def test_sign_missing_msg(client: TestClient):
    response = client.post('/sign', json={})
    assert response.status_code == 422


def test_verify_success(client: TestClient):
    sign_response = client.post('/sign', json={'msg': 'test message'})
    assert sign_response.status_code == 200
    signature = sign_response.json()['signature']

    verify_response = client.post(
        '/verify',
        json={'msg': 'test message', 'signature': signature},
    )
    assert verify_response.status_code == 200
    assert verify_response.json()['ok'] is True


def test_verify_modified_message(client: TestClient):
    sign_response = client.post('/sign', json={'msg': 'hello'})
    signature = sign_response.json()['signature']

    verify_response = client.post(
        '/verify',
        json={'msg': 'hello!', 'signature': signature},
    )
    assert verify_response.status_code == 200
    assert verify_response.json()['ok'] is False


def test_verify_invalid_signature(client: TestClient):
    sign_response = client.post('/sign', json={'msg': 'hello'})
    signature = sign_response.json()['signature']

    modified_sig = signature[:-1] + ('A' if signature[-1] != 'A' else 'B')

    verify_response = client.post(
        '/verify',
        json={'msg': 'hello', 'signature': modified_sig},
    )
    assert verify_response.status_code == 200
    assert verify_response.json()['ok'] is False


def test_verify_invalid_signature_format(client: TestClient):
    response = client.post(
        '/verify',
        json={'msg': 'hello', 'signature': '@@@invalid@@@'},
    )
    assert response.status_code == 400
    assert response.json()['detail'] == 'invalid_signature_format'


def test_verify_empty_message(client: TestClient):
    response = client.post(
        '/verify',
        json={'msg': '', 'signature': 'dGVzdA'},
    )
    assert response.status_code == 422


def test_verify_missing_fields(client: TestClient):
    response = client.post('/verify', json={})
    assert response.status_code == 422


def test_large_message(client: TestClient):
    large_msg = 'x' * (1048576 + 1)
    response = client.post('/sign', json={'msg': large_msg})
    assert response.status_code == 413


def test_deterministic_signature(client: TestClient):
    response1 = client.post('/sign', json={'msg': 'deterministic test'})
    response2 = client.post('/sign', json={'msg': 'deterministic test'})

    sig1 = response1.json()['signature']
    sig2 = response2.json()['signature']

    assert sig1 == sig2


def test_unicode_message(client: TestClient):
    msg = 'Привет, мир! 👋'

    sign_response = client.post('/sign', json={'msg': msg})
    assert sign_response.status_code == 200
    signature = sign_response.json()['signature']

    verify_response = client.post(
        '/verify',
        json={'msg': msg, 'signature': signature},
    )
    assert verify_response.status_code == 200
    assert verify_response.json()['ok'] is True
