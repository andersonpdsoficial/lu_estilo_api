import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database.database import Base, get_db

DATABASE_URL = "postgresql://postgres:628629@localhost:5432/lu_estilo_test"
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def auth_token():
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

def test_create_order(auth_token, create_product, create_client):
    response = client.post(
        "/orders/",
        json={
            "client_id": create_client,
            "items": [{"product_id": create_product, "quantity": 2}]
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    assert response.json()["client_id"] == create_client