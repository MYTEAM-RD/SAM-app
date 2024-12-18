import datetime
from .conftest import client, client_with_user, client_with_admin
import random
import string
import jwt
import os


def test_login(client_with_user):
    response = client_with_user.post(
        "/api/v1/login", json={"email": "test@gmail.com", "password": "Password1"}
    )
    assert response.status_code == 200
    assert response.json["token"] is not None


def test_login_admin(client_with_admin):
    response = client_with_admin.post(
        "/api/v1/login", json={"email": "test@gmail.com", "password": "Password1"}
    )
    assert response.status_code == 200
    assert response.json["token"] is not None
    token = jwt.decode(
        response.json["token"], os.environ.get("SECRET_KEY"), algorithms=["HS256"]
    )
    assert token["scope"] == "admin"


def test_login_fail_bad_email(client_with_user):
    response = client_with_user.post(
        "/api/v1/login", json={"email": "lala@gmail.com", "password": "test"}
    )
    assert response.status_code == 400


def test_login_fail_bad_password(client_with_user):
    response = client_with_user.post(
        "/api/v1/login", json={"email": "test@gmail.com", "password": "lala"}
    )
    assert response.status_code == 401


def test_token_check(client_with_user):
    response = client_with_user.post(
        "/api/v1/login", json={"email": "test@gmail.com", "password": "Password1"}
    )
    assert response.status_code == 200
    response = client_with_user.get(
        "/api/v1/check", headers={"Authorization": "Bearer " + response.json["token"]}
    )
    assert response.status_code == 200


def test_check_fail(client):
    response = client.get("/api/v1/check", headers={"Authorization": "laala"})
    assert response.status_code == 401


def test_wrong_signature(client_with_user):
    encoded_jwt = jwt.encode(
        {
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=14),
            "iat": datetime.datetime.utcnow(),
            "nbf": datetime.datetime.utcnow(),
            "scope": "admin",
            "id": "3ab49c23-120b-4294-89df-27ad88deaf15",
            "email_verified": True,
        },
        "fakekey",
        algorithm="HS256",
    )
    response = client_with_user.get(
        "/api/v1/check", headers={"Authorization": "Bearer " + encoded_jwt}
    )
    assert response.status_code == 401
