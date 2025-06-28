from fastapi.testclient import TestClient
from data.account_data import accounts_list
from data.transaction_data import transaction_list
from data.user_data import user_list

def seed_db(db):
    db.commit()
    db.add_all(user_list)
    db.commit()
    db.add_all(accounts_list)
    db.commit()
    db.add_all(transaction_list)
    db.commit()

def login(test_app: TestClient, username: str, password: str):
    response = test_app.post("/api/login", json={"username": username, "password": password})

    if response.status_code != 200:
        raise Exception(f"Login failed: {response.json().get('detail', 'Unknown error')}")

    token = response.json().get('token')
    if not token:
        raise Exception("No token returned from login endpoint.")

    headers = {"Authorization": f"Bearer {token}"}
    return headers

