import pytest
from fastapi.testclient import TestClient
from main import app  # ✅ correct
client = TestClient(app)

def test_register_user_success():
    response = client.post("/register", json={
        "username": "zainab_test_1",
        "email": "zainab_test_1@example.com",
        "password": "strongpassword123",
        "is_admin": False,
        "created_at": "2025-06-24T20:00:00"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "zainab_test_1"
    assert data["email"] == "zainab_test_1@example.com"

def test_register_existing_user():
    # First registration
    client.post("/register", json={
        "username": "zainab_existing",
        "email": "zainab_existing@example.com",
        "password": "mypass",
        "is_admin": False,
        "created_at": "2025-06-24T20:00:00"
    })

    # Attempt to re-register same username/email
    response = client.post("/register", json={
        "username": "zainab",
        "email": "zainab@kpmg.com",
        "password": "123456",
        "is_admin": False,
        "created_at": "2025-06-24T20:00:00"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Username or email already exists"