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

'''


@router.get("/accounts/me")
def get_my_account(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    account = db.query(AccountModel).filter(AccountModel.user_id == current_user.id).first()
    
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    return {
        "id": account.id,
        "balance": account.balance,
        "created_at": account.created_at,
    }