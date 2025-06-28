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
    raw_transactions = db.query(TransactionModel).filter(
        (TransactionModel.sender_id == current_user.id) |
        (TransactionModel.recipient_id == current_user.id)
    ).order_by(TransactionModel.created_at.desc()).all()

    result = []
    for z in raw_transactions:
        direction = "sent" if z.sender_id == current_user.id else "received"
        result.append({
            "id": z.id,
            "sender_id": z.sender_id,
            "recipient_id": z.recipient_id,
            "amount": z.amount,
            "created_at": z.created_at,
            "direction": direction
        })

    return result


@router.get("/transactions/{user_id}", response_model=List[TransactionSchema])
def view_user_transactions(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Access denied: admin only")

    transactions = db.query(TransactionModel).filter(
        (TransactionModel.sender_id == user_id) |
        (TransactionModel.recipient_id == user_id)
    ).order_by(TransactionModel.created_at.desc()).all()

    return transactions 