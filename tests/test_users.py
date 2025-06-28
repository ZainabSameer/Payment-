import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from models.user import UserModel
from tests.lib import login
from main import app

client = TestClient(app)


def test_register_user_success(test_app: TestClient, override_get_db):
    response = client.post("/api/register", json={
        "username": "zainab_test1",
        "email": "zainab_test1@kpmg.com",
        "password": "strongpassword123",
        "is_admin": False,
        "created_at": "2025-06-25T21:00:00"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "zainab_test1"
    assert data["email"] == "zainab_test1@kpmg.com"

def test_register_user_duplicate(test_app: TestClient, override_get_db):
    client.post("/api/register", json={
        "username": "zainab_d",
        "email": "zainab_d@kpmg.com",
        "password": "password456",
        "is_admin": False,
        "created_at": "2025-06-25T21:00:00"
    })

    response = client.post("/api/register", json={
        "username": "zainab_d",
        "email": "zainab_d@kpmg.com",
        "password": "password456",
        "is_admin": False,
        "created_at": "2025-06-25T21:00:00"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Username or email already exists"