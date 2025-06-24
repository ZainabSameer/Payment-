from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.user import UserModel
from serializers.user import UserSchema, UserLogin, UserToken, UserResponseSchema
from database import get_db
from dependencies.get_current_user import get_current_user

from models.account import AccountModel
router = APIRouter()

@router.post("/register", response_model=UserResponseSchema)
def create_user(user: UserSchema, db: Session = Depends(get_db)):
    existing_user = db.query(UserModel).filter(
        (UserModel.username == user.username) | (UserModel.email == user.email)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already exists")

    new_user = UserModel(username=user.username, email=user.email, is_admin=user.is_admin)
    new_user.set_password(user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    new_account = AccountModel(user_id=new_user.id, balance=0.00, currency="USD")
    db.add(new_account)
    db.commit()

    return new_user

@router.post("/login", response_model=UserToken)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.username == user.username).first()
    if not db_user or not db_user.verify_password(user.password):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    token = db_user.generate_token()
    return {"token": token, "message": "Login successful"}

@router.get("/users/me")
def get_user_profile(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    user = db.query(UserModel).filter(UserModel.id == current_user.id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    account = db.query(AccountModel).filter(AccountModel.user_id == user.id).first()

    return {
        "username": user.username,
        "email": user.email,
        "account_id": account.id if account else None
    }