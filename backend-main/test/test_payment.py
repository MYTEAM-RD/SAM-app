from app.models.user import User
from .conftest import (
    client,
    client_with_user,
    generate_token_user,
    client_with_user_payment_wating,
)


def test_get_all_products(client):
    response = client.get(
        "/api/v1/products",
    )
    assert response.status_code == 200


def test_get_products_and_price(client):
    response = client.get(
        "/api/v1/products",
    )
    assert response.status_code == 200
    for item in response.json["data"]:
        response2 = client.get(
            f"/api/v1/price/{item['default_price']}",
        )
        assert response2.status_code == 200


def test_get_user_portal(client_with_user):
    enconded_jwt = generate_token_user(
        User(
            "test@gmail.com",
            "lucas",
            "Password1",
            email_verified=True,
            id="3ab49c23-120b-4294-89df-27ad88deaf15",
            credit=10,
        )
    )
    response = client_with_user.get(
        "/api/v1/customer_portal",
        headers={"Authorization": enconded_jwt},
    )
    assert response.status_code == 200


def test_get_succes_subscription(client_with_user_payment_wating):
    response = client_with_user_payment_wating.get(
        "/api/v1/sucess_payment/6666/?redirect_url=https://example.com/sucess",
    )
    assert response.status_code == 302
    assert response.location == "https://example.com/sucess"

def test_create_checkout_session_all_items(client_with_user):
    enconded_jwt = generate_token_user(
        User(
            "test@gmail.com",
            "lucas",
            "Password1",
            email_verified=True,
            id="3ab49c23-120b-4294-89df-27ad88deaf15",
            credit=10,
        )
    )
    response = client_with_user.get(
        "/api/v1/products",
    )
    assert response.status_code == 200
    data = {
        "items": [],
        "success_url": "https://example.com/sucess",
        "cancel_url": "https://example.com/cancel",
    }
    for item in response.json["data"]:
        data["items"].append({"id": item["id"], "quantity": 1})
    response2 = client_with_user.post(
        "/api/v1/create_payment", json=data, headers={"Authorization": enconded_jwt}
    )
    assert response2.status_code == 200


def test_create_checkout_session_payment(client_with_user):
    enconded_jwt = generate_token_user(
        User(
            "test@gmail.com",
            "lucas",
            "Password1",
            email_verified=True,
            id="3ab49c23-120b-4294-89df-27ad88deaf15",
            credit=10,
        )
    )
    response = client_with_user.get(
        "/api/v1/products",
    )
    assert response.status_code == 200
    data = {
        "items": [{"id": "prod_ODkJ2EIXK3DD8U", "quantity": 3}],
        "success_url": "https://example.com/sucess",
        "cancel_url": "https://example.com/cancel",
    }
    response2 = client_with_user.post(
        "/api/v1/create_payment", json=data, headers={"Authorization": enconded_jwt}
    )
    assert response2.status_code == 200


def test_create_checkout_session_subscription(client_with_user):
    enconded_jwt = generate_token_user(
        User(
            "test@gmail.com",
            "lucas",
            "Password1",
            email_verified=True,
            id="3ab49c23-120b-4294-89df-27ad88deaf15",
            credit=10,
        )
    )
    response = client_with_user.get(
        "/api/v1/products",
    )
    assert response.status_code == 200
    data = {
        "items": [{"id": "prod_ODkamv9ll9Ter3", "quantity": 1}],
        "success_url": "https://example.com/sucess",
        "cancel_url": "https://example.com/cancel",
    }
    response2 = client_with_user.post(
        "/api/v1/create_payment", json=data, headers={"Authorization": enconded_jwt}
    )
    assert response2.status_code == 200
