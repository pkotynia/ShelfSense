import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text  # Added text import for raw SQL execution
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.models import Base, engine, SessionLocal
from app.dependencies import get_db
import uuid

# Use a test database (in-memory or a dedicated test DB)
# For demonstration, we'll use the same engine, but in real projects use a separate DB!

@pytest.fixture(scope="module")
def test_client():
    # Create tables
    Base.metadata.create_all(bind=engine)
    client = TestClient(app)
    yield client
    # Drop tables after tests
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(autouse=True)
def clear_users():
    # Clean up users table before each test
    db = SessionLocal()
    db.execute(text("DELETE FROM shelfsense.users"))  # Use text() for raw SQL
    db.commit()
    db.close()


def test_register_success(test_client):
    payload = {"email": "testuser@example.com", "password": "Password123"}
    response = test_client.post("/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["email"] == payload["email"]
    assert "token" in data


def test_register_duplicate_email(test_client):
    payload = {"email": "dupe@example.com", "password": "Password123"}
    # First registration
    response1 = test_client.post("/auth/register", json=payload)
    assert response1.status_code == 201
    # Second registration with same email
    response2 = test_client.post("/auth/register", json=payload)
    assert response2.status_code == 409
    assert "Email already exists" in response2.text


def test_register_invalid_password(test_client):
    payload = {"email": "badpass@example.com", "password": "short"}
    response = test_client.post("/auth/register", json=payload)
    assert response.status_code == 422  # Pydantic validation error

    payload2 = {"email": "badpass2@example.com", "password": "allletters"}
    response2 = test_client.post("/auth/register", json=payload2)
    assert response2.status_code == 422 or response2.status_code == 400
    # Should mention password complexity
    assert "Password must contain both letters and numbers" in response2.text


def test_register_invalid_email(test_client):
    payload = {"email": "notanemail", "password": "Password123"}
    response = test_client.post("/auth/register", json=payload)
    assert response.status_code == 422
    assert "value is not a valid email address" in response.text
