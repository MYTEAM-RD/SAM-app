from .conftest import client_with_user_unverified, generate_token_user
from app.models.user import User
import random
import string
import jwt
import os


def test_verify_email(client_with_user_unverified):
    response = client_with_user_unverified.get("/api/v1/verify/email?code=0000")
    assert response.status_code == 200


def test_verify_email_wrong_code(client_with_user_unverified):
    response = client_with_user_unverified.get("/api/v1/verfify/email?code=2222")
    assert response.status_code == 404


def test_verify_email_with_phone_code(client_with_user_unverified):
    response = client_with_user_unverified.get("/api/v1/verfify/email?code=1111")
    assert response.status_code == 404


def test_verify_phone_with_email_code(client_with_user_unverified):
    response = client_with_user_unverified.get("/api/v1/verfify/phone?code=0000")
    assert response.status_code == 404


def test_verify_phone_wrong_code(client_with_user_unverified):
    response = client_with_user_unverified.get("/api/v1/verfify/email?code=2222")
    assert response.status_code == 404


def test_ask_new_email_code(client_with_user_unverified):
    enconded_jwt = generate_token_user(
        User(
            "test@gmail.com",
            "lucas",
            "Password1",
            email_verified=False,
            id="3ab49c23-120b-4294-89df-27ad88deaf15",
        )
    )
    response = client_with_user_unverified.get(
        "/api/v1/verify/new/email", headers={"Authorization": enconded_jwt}
    )
    assert response.status_code == 200
