from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_login_success():
    client.post("/api/register", json={
        "username": "zainab_login",
        "email": "zainab_login@kpmg.com",
        "password": "secret123",
        "is_admin": False,
        "created_at": "2025-06-25T21:00:00"
    })

    response = client.post("/api/login", json={
        "username": "zainab_login",
        "password": "secret123"
    })

    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert data["message"] == "Login successful"

def test_login_invalid_credentials():
    response = client.post("/api/login", json={
        "username": "zainab_wrong",
        "password": "incorrect"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid username or password"