from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.transaction import TransactionModel
from models.account import AccountModel
from models.user import UserModel
from serializers.transaction import TransactionCreate, TransactionSchema
from database import get_db
from dependencies.get_current_user import get_current_user
from typing import List
from datetime import datetime

router = APIRouter()

@router.post("/transactions/send", response_model=TransactionSchema)
def send_money(
    data: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    sender_account = db.query(AccountModel).filter(AccountModel.user_id == current_user.id).first()
    recipient_account = db.query(AccountModel).filter(AccountModel.user_id == data.recipient_id).first()

    if not recipient_account:
        raise HTTPException(status_code=404, detail="Recipient account not found")

    if not sender_account or sender_account.balance < data.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    # Perform transfer
    sender_account.balance -= data.amount
    recipient_account.balance += data.amount

    transaction = TransactionModel(
        sender_id=current_user.id,
        recipient_id=data.recipient_id,
        amount=data.amount,

    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction

@router.get("/transactions/history", response_model=List[TransactionSchema])
def get_transaction_history(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    transactions = db.query(TransactionModel).filter(
        (TransactionModel.sender_id == current_user.id) |
        (TransactionModel.recipient_id == current_user.id)
    ).order_by(TransactionModel.created_at.desc()).all()

    return transactions
