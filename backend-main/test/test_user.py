from app.models.user import User
from .conftest import (
    client,
    client_with_user,
    client_with_user_password_forgotten,
    generate_token_admin,
    generate_token_user,
)
import random
import string


def test_create_user(client):
    response = client.post(
        "/api/v1/user",
        json={
            "email": "".join(random.choices(string.ascii_letters + string.digits, k=10))
            + "@gmail.com",
            "password": "Password1",
            "name": "test",
        },
    )
    assert response.status_code == 200


def test_create_user_full(client):
    response = client.post(
        "/api/v1/user",
        json={
            "email": "".join(random.choices(string.ascii_letters + string.digits, k=10))
            + "@gmail.com",
            "password": "Password1",
            "name": "test",
            "phone": "".join(random.choices(string.digits, k=10)),
            "company": "test",
            "company_type": "test",
        },
    )
    assert response.status_code == 200
    assert response.json["company"] == "test"
    assert response.json["company_type"] == "test"
    assert response.json["email_verified"] == "False"


def test_create_user_without_password(client):
    response = client.post(
        "/api/v1/user",
        json={
            "email": "".join(random.choices(string.ascii_letters + string.digits, k=10))
            + "@gmail.com",
            "name": "test",
            "phone": "".join(random.choices(string.digits, k=10)),
        },
    )
    assert response.status_code == 400


def test_create_user_without_name_and_phone(client):
    response = client.post(
        "/api/v1/user",
        json={
            "email": "".join(random.choices(string.ascii_letters + string.digits, k=10))
            + "@gmail.com",
            "password": "Password1",
        },
    )
    assert response.status_code == 200


def test_update_user_name(client_with_user):
    response = client_with_user.post(
        "/api/v1/login", json={"email": "test@gmail.com", "password": "Password1"}
    )
    assert response.status_code == 200
    response = client_with_user.patch(
        "/api/v1/user",
        json={
            "name": "test",
        },
        headers={"Authorization": "Bearer " + response.json["token"]},
    )
    assert response.status_code == 200
    assert response.json["name"] == "test"


def test_get_personal_info(client_with_user):
    enconded_jwt = generate_token_user(
        User(
            "test@gmail.com",
            "lucas",
            "Password1",
            email_verified=True,
            id="3ab49c23-120b-4294-89df-27ad88deaf15",
            credit=0,
        )
    )
    response = client_with_user.get(
        "/api/v1/user/me", headers={"Authorization": enconded_jwt}
    )
    assert response.status_code == 200
    assert response.json["email"] == "test@gmail.com"
    assert response.json["name"] == "lucas"
    assert response.json["credit"] == "0"
    assert response.json["email_verified"] == "True"


def test_update_user_info(client_with_user):
    response = client_with_user.post(
        "/api/v1/login", json={"email": "test@gmail.com", "password": "Password1"}
    )
    assert response.status_code == 200
    response = client_with_user.patch(
        "/api/v1/user",
        json={
            "name": "test",
            "phone": "0123456789",
            "address": "test address",
            "company": "test company",
            "company_type": "test company type",
        },
        headers={"Authorization": "Bearer " + response.json["token"]},
    )
    assert response.status_code == 200
    assert response.json["name"] == "test"


def test_update_user_password(client_with_user):
    response = client_with_user.post(
        "/api/v1/login", json={"email": "test@gmail.com", "password": "Password1"}
    )
    assert response.status_code == 200
    response = client_with_user.patch(
        "/api/v1/user",
        json={
            "password": "Newpassword1",
        },
        headers={"Authorization": "Bearer " + response.json["token"]},
    )
    assert response.status_code == 200
    response = client_with_user.post(
        "/api/v1/login", json={"email": "test@gmail.com", "password": "Newpassword1"}
    )
    assert response.status_code == 200
    assert response.json["token"] is not None


def test_update_user_password_without_token(client):
    response = client.patch(
        "/api/v1/user",
        json={
            "password": "newpassword",
        },
    )
    assert response.status_code == 401


def test_update_user_password_with_bad_token(client):
    response = client.patch(
        "/api/v1/user",
        json={
            "password": "newpassword",
        },
        headers={"Authorization": "fake token"},
    )
    assert response.status_code == 401


def test_update_email(client_with_user):
    response = client_with_user.post(
        "/api/v1/login", json={"email": "test@gmail.com", "password": "Password1"}
    )
    assert response.status_code == 200
    new_email = (
        "".join(random.choices(string.ascii_letters + string.digits, k=10))
        + "@gmail.com"
    )
    response = client_with_user.patch(
        "/api/v1/user/email",
        json={
            "email": new_email,
        },
        headers={"Authorization": "Bearer " + response.json["token"]},
    )
    assert response.status_code == 200
    response = client_with_user.post(
        "/api/v1/login", json={"email": new_email, "password": "Password1"}
    )
    assert response.status_code == 200
    assert response.json["token"] is not None


def test_delete_user(client_with_user):
    response = client_with_user.post(
        "/api/v1/login", json={"email": "test@gmail.com", "password": "Password1"}
    )
    assert response.status_code == 200
    response = client_with_user.delete(
        "/api/v1/user", headers={"Authorization": "Bearer " + response.json["token"]}
    )
    assert response.status_code == 200
    response = client_with_user.post(
        "/api/v1/login", json={"email": response.json["email"], "password": "test"}
    )
    assert response.status_code == 400


def test_password_forgotten(client_with_user):
    response = client_with_user.get(
        "/api/v1/trouble/forgot_email?email=test@gmail.com",
    )
    assert response.status_code == 200


def test_password_forgotten_wrong_email(client_with_user):
    response = client_with_user.get(
        "/api/v1/trouble/forgot_email?email=lala",
    )
    assert response.status_code == 404


def test_password_forgotten_then_modify_email(client_with_user_password_forgotten):
    response = client_with_user_password_forgotten.post(
        "/api/v1/trouble/forgot_email",
        json={"password": "NewPassword1", "code": "5555"},
    )
    assert response.status_code == 200


def test_password_forgotten_then_modify_email_invalid_password(
    client_with_user_password_forgotten,
):
    response = client_with_user_password_forgotten.post(
        "/api/v1/trouble/forgot_email", json={"password": "lala", "code": "5555"}
    )
    assert response.status_code == 400


def test_admin_delete_user(client_with_admin):
    encoded_jwt = generate_token_admin(
        User(
            "test@gmail.com",
            "lucas",
            "Password1",
            _type="admin",
            email_verified=True,
            id="3ab49c23-120b-4294-89df-27ad88deaf15",
        )
    )
    response = client_with_admin.delete(
        "/api/v1/user/3ab49c23-120b-4294-89df-27ad88deaf15",
        headers={"Authorization": encoded_jwt},
    )
    assert response.status_code == 200
