from .conftest import client


def test_contact_successful(client):
    response = client.post(
        "/api/v1/contact",
        json={
            "from": "user@example.com",
            "subject": "Test Subject",
            "phone": "1234567890",
            "content": "Test Content",
        },
    )
    assert response.status_code == 200
    assert response.data == b"sended"


def test_contact_missing_from(client):
    response = client.post(
        "/api/v1/contact",
        json={
            "subject": "Test Subject",
            "phone": "1234567890",
            "content": "Test Content",
        },
    )
    assert response.status_code == 400
    assert response.data == b"you have to provide a from"


def test_contact_missing_subject(client):
    response = client.post(
        "/api/v1/contact",
        json={
            "from": "user@example.com",
            "phone": "1234567890",
            "content": "Test Content",
        },
    )
    assert response.status_code == 400
    assert response.data == b"you have to provide an subject"


def test_contact_missing_phone(client):
    response = client.post(
        "/api/v1/contact",
        json={
            "from": "user@example.com",
            "subject": "Test Subject",
            "content": "Test Content",
        },
    )
    assert response.status_code == 400
    assert response.data == b"you have to provide an phone"


def test_contact_missing_content(client):
    response = client.post(
        "/api/v1/contact",
        json={
            "from": "user@example.com",
            "subject": "Test Subject",
            "phone": "1234567890",
        },
    )
    assert response.status_code == 400
    assert response.data == b"you have to provide an content"
