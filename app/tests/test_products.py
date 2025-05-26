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

def test_create_product(client, auth_token):
    response = client.post(
        "/products/",
        json={
            "description": "Produto Teste",
            "price": 10.0,
            "barcode": "1234567890123",
            "section": "A",
            "stock": 10
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    assert response.json()["description"] == "Produto Teste"

def test_create_product_invalid_barcode(client, auth_token):
    response = client.post(
        "/products/",
        json={
            "description": "Produto Teste",
            "price": 10.0,
            "barcode": "invalid",
            "section": "A",
            "stock": 10
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 400