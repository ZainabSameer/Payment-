from models.transaction import TransactionModel
from datetime import datetime

transaction_list = [
    TransactionModel(sender_id=1, recipient_id=2, amount=100.0, created_at=datetime.utcnow()),
    TransactionModel(sender_id=2, recipient_id=1, amount=50.0, created_at=datetime.utcnow())
]