import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from models.account import AccountModel
from tests.lib import login
from main import app

client = TestClient(app)
'''
def test_get_my_account_balance(test_app: TestClient, test_db: Session, override_get_db):
    client.post("/api/register", json={
        "username": "zainab_balance",
        "email": "balance_user@kpmg.com",
        "password": "securepass123",
        "is_admin": False
    })

    login_response = client.post("/api/login", json={
        "username": "zainab_balance",
        "password": "securepass123"
    })

    assert login_response.status_code == 200
    token = login_response.json()["token"]

    response = client.get(
        "/api/accounts/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()

    assert data["user_id"] is not None
    assert isinstance(data["balance"], float)
  ------------------

def test_get_my_account_balance(test_app: TestClient, test_db: Session, override_get_db):
    register_response = client.post("/api/register", json={
        "username": "zainab_balance",
        "email": "balance_user@kpmg.com",
        "password": "securepass123",
        "is_admin": False,
        "created_at": "2025-06-28T15:00:00"
    })

    assert register_response.status_code == 200

    login_response = client.post("/api/login", json={
        "username": "zainab_balance",
        "password": "securepass123"
    })

    assert login_response.status_code == 200
    token = login_response.json()["token"]

    response = client.get(
        "/api/accounts/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()

    assert data["user_id"] is not None
    assert isinstance(data["balance"], float)

    '''


def test_get_my_account_balance():
    register_response = client.post("/api/register", json={
        "username": "zainab_testacct",
        "email": "acct_user@kpmg.com",
        "password": "testpass123",
        "is_admin": False,
        "created_at": "2025-06-28T15:00:00"
    })
    assert register_response.status_code == 200

    login_response = client.post("/api/login", json={
        "username": "zainab_testacct",
        "password": "testpass123"
    })
    assert login_response.status_code == 200
    token = login_response.json()["token"]

    response = client.get("/api/accounts/me", headers={
        "Authorization": f"Bearer {token}"
    })

    assert response.status_code == 200
    data = response.json()
    print("Balance response data:", data)

    assert data["id"] is not None
    assert isinstance(data["balance"], float)