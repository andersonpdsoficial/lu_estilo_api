import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database.database import get_db
from app.tests.conftest import get_test_db, setup_test_database

app.dependency_overrides[get_db] = get_test_db
client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    yield from setup_test_database()

@pytest.fixture
def auth_token(client):
    client.post("/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword"
    })
    response = client.post("/auth/login", data={
        "username": "testuser",
        "password": "testpassword"
    })
    return response.json()["access_token"]

def test_create_client(client, auth_token):
    response = client.post(
        "/clients/",
        json={
            "name": "Test Client",
            "email": "client@example.com",
            "cpf": "12345678901",
            "phone": "+5511999999999"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Test Client"

def test_create_client_invalid_cpf(client, auth_token):
    response = client.post(
        "/clients/",
        json={
            "name": "Test Client",
            "email": "client@example.com",
            "cpf": "invalid",
            "phone": "+5511999999999"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid CPF"

def test_list_clients(client, auth_token):
    client.post(
        "/clients/",
        json={
            "name": "Test Client",
            "email": "client@example.com",
            "cpf": "12345678901",
            "phone": "+5511999999999"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    response = client.get("/clients/", headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 200
    assert len(response.json()) > 0