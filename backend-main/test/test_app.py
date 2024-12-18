from .conftest import client


def test_app_online(client):
    response = client.get("api/v1/health")
    assert response.status_code == 200
