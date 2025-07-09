# Zainab Bank API

A secure, modular banking backend built with **FastAPI**. Users can register, log in with JWT-based authentication, manage their accounts, transfer funds, and view transaction history.

---

## Getting Started
1. clone the repo
2. inastall dependencies --> **pipenv install**
3. run the app --> **uvicorn main:app --reload**
4. access the api --> **http://localhost:8000**

   
###  Technologies Used 
- FastAPI
- SQLAlchemy
- PassLib
- PyJWT
- PyTest

### 🔐 Auth Routes

| HTTP Method | Endpoint       | Description                     | Access Level | Notes                        |
|-------------|----------------|---------------------------------|---------------|------------------------------|
| POST        | `/auth/signup` | Register a new user             | Public        | Stores hashed password       |
| POST        | `/auth/login`  | Log in and receive JWT token    | Public        | Returns access token         |

### 👤 User & Account Routes

| HTTP Method | Endpoint        | Description                      | Access Level     | Notes                                      |
|-------------|------------------|----------------------------------|------------------|--------------------------------------------|
| GET         | `/users/me`      | Get current user’s profile       | Logged-in users  | Returns username, email, and account ID    |
| GET         | `/accounts/me`   | View current user’s account info | Logged-in users  | Shows balance, currency, and account details |

### 💸 Transaction Routes

| HTTP Method | Endpoint               | Description                          | Access Level     | Notes                                                                 |
|-------------|------------------------|--------------------------------------|------------------|-----------------------------------------------------------------------|
| POST        | `/transactions/send`   | Transfer money to another user       | Logged-in users  | Requires sender ID, recipient ID, and amount. Prevents overdrafts.    |
| GET         | `/transactions/history`| View transaction history             | Logged-in users  | Users can only view their own transactions (sent & received)          |

### 🚨 Admin 

| HTTP Method | Endpoint                     | Description                          | Access Level | Notes                                        |
|-------------|------------------------------|--------------------------------------|--------------|----------------------------------------------|
| GET         | `/transactions/{user_id}`    | View another user’s transactions     | Admins only  | For monitoring fraud or resolving disputes   |

### Attributions
This project was built with guidance from:
- The official FastAPI documentation
- Old projects and labs " teas , library, .. "

