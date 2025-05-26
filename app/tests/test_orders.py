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

@pytest.fixture
def create_product(auth_token):
    response = client.post(
        "/products/",
        json={
            "description": "Test Product",
            "price": 99.99,
            "barcode": "123456789012",
            "section": "Clothing",
            "stock": 10
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    return response.json()["id"]

@pytest.fixture
def create_client(auth_token):
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
    return response.json()["id"]

def test_create_order(client, auth_token):
    # Crie um cliente primeiro
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
    # Crie o pedido
    response = client.post(
        "/orders/",
        json={
            "client_id": 1,
            "items": []
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    assert response.json()["client_id"] == 1