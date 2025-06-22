from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.account import AccountModel
from models.user import UserModel
from serializers.account import AccountSchema, AccountCreate as AccountCreateSchema , AccountUpdate
from typing import List
from database import get_db
from dependencies.get_current_user import get_current_user

router = APIRouter()

@router.get("/accounts", response_model=List[AccountSchema])
def get_accounts(db: Session = Depends(get_db)):
    accounts = db.query(AccountModel).all()
    return accounts

@router.get("/accounts/{account_id}", response_model=AccountSchema)
def get_single_account(account_id: int, db: Session = Depends(get_db)):
    account = db.query(AccountModel).filter(AccountModel.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account

@router.post("/accounts", response_model=AccountSchema)
def create_account(account: AccountCreateSchema, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    new_account = AccountModel(**account.model_dump(), user_id=current_user.id)
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    return new_account

@router.put("/accounts/{account_id}", response_model=AccountSchema)
def update_account(account_id: int, account: AccountUpdate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    db_account = db.query(AccountModel).filter(AccountModel.id == account_id).first()
    if not db_account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    if db_account.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Operation forbidden")

    account_data = account_data = account.model_dump(exclude_unset=True)
    for key, value in account_data.items():
        setattr(db_account, key, value)

    db.commit() 
    db.refresh(db_account)  
    return db_account


@router.delete("/accounts/{account_id}")
def delete_account(account_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    db_account = db.query(AccountModel).filter(AccountModel.id == account_id).first()
    if not db_account:
        raise HTTPException(status_code=404, detail="not found")

    if db_account.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Operation forbidden")

    db.delete(db_account)
    db.commit()
    return {"message": f"Account with ID {account_id} has been deleted"}