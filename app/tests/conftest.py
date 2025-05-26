import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.base import Base
from app.database.database import get_db, get_database
from app.main import app
from fastapi.testclient import TestClient

# Test database URL
TEST_DATABASE_URL = "postgresql://postgres:123456@localhost:5433/lu_estilo_test"

# Override the DATABASE_URL environment variable for tests
os.environ["DATABASE_URL"] = TEST_DATABASE_URL

@pytest.fixture(scope="session")
def test_engine():
    # Create test database engine using the factory function
    engine, _ = get_database()
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    yield engine
    
    # Drop all tables after tests
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session(test_engine):
    # Create a new session for each test
    Session = sessionmaker(bind=test_engine)
    session = Session()
    
    try:
        yield session
    finally:
        session.rollback()
        session.close()

@pytest.fixture(scope="function")
def client(db_session):
    # Override the get_db dependency
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Clear dependency overrides
    app.dependency_overrides.clear() 