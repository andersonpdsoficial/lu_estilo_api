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

def test_create_client(auth_token):
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

def test_create_client_invalid_cpf(auth_token):
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

def test_list_clients(auth_token):
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