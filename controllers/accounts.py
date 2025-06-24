from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from models.account import AccountModel
from models.user import UserModel
from serializers.account import AccountSchema, AccountCreate as AccountCreateSchema, AccountUpdate
from database import get_db
from dependencies.get_current_user import get_current_user

router = APIRouter()
'''
@router.get("/accounts/{account_id}", response_model=AccountSchema)
def get_single_account(
    account_id: int,
    db: Session = Depends(get_db)
):
    account = (
        db.query(AccountModel)
        .filter(AccountModel.id == account_id)
        .first()
    )
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account

@router.post("/accounts", response_model=AccountSchema)
def create_account(
    account: AccountCreateSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    new_account = AccountModel(
        user_id=current_user.id,
        balance=account.balance,
        currency=account.currency
    )
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    return new_account


---
@router.get("/accounts/me", response_model=AccountSchema)
def get_single_account(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    account = (
        db.query(AccountModel)
        .filter(AccountModel.user_id == current_user.id)
        .first()
    )
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account
'''
@router.get("/accounts/me")
def get_account_details(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    account = db.query(AccountModel).filter(AccountModel.user_id == current_user.id).first()

    if not account:
        raise HTTPException(status_code=404, detail="No account found for this user")

    return {
        "id": account.id,
        "balance": account.balance,
        "currency": account.currency
    }