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


def test_register_then_login(test_client):
    # Register a new user
    register_payload = {"email": "flowuser@example.com", "password": "FlowPassword1"}
    reg_resp = test_client.post("/auth/register", json=register_payload)
    assert reg_resp.status_code == 201
    reg_data = reg_resp.json()
    assert "id" in reg_data
    user_id = reg_data["id"]
    # Login with the same credentials
    login_payload = {"email": register_payload["email"], "password": register_payload["password"]}
    login_resp = test_client.post("/auth/login", json=login_payload)
    assert login_resp.status_code == 200
    login_data = login_resp.json()
    print("Login data:", login_data)
    # Verify response contains expected fields
    assert login_data["id"] == user_id
    assert login_data["email"] == register_payload["email"]
    assert "token" in login_data


def test_login_invalid_credentials(test_client):
    # Attempt login without registering
    bad_login = {"email": "nouser@example.com", "password": "NoUserPass1"}
    resp = test_client.post("/auth/login", json=bad_login)
    assert resp.status_code == 401
    # Should indicate invalid credentials
    assert "Invalid credentials" in resp.json().get("detail", "")


def test_register_login_and_add_preferences(test_client):
    # Register a new user
    register_payload = {"email": "prefuser@example.com", "password": "PrefPass123"}
    reg_resp = test_client.post("/auth/register", json=register_payload)
    assert reg_resp.status_code == 201
    # Login to get JWT token
    login_resp = test_client.post(
        "/auth/login", json={"email": register_payload["email"], "password": register_payload["password"]}
    )
    assert login_resp.status_code == 200
    token = login_resp.json()["token"]
    # Add or update preferences
    prefs_payload = {"preferences_text": "dark mode enabled"}
    put_resp = test_client.put(
        "/users/me/preferences",
        headers={"Authorization": f"Bearer {token}"},
        json=prefs_payload
    )
    assert put_resp.status_code == 200
    prefs_data = put_resp.json()
    assert "id" in prefs_data
    assert prefs_data["preferences_text"] == prefs_payload["preferences_text"]
    assert "updated_at" in prefs_data
    # Fetch preferences back
    get_resp = test_client.get(
        "/users/me/preferences",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert get_resp.status_code == 200
    get_data = get_resp.json()
    assert get_data == prefs_data
