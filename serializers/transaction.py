from pydantic import BaseModel
from datetime import datetime


class TransactionCreate(BaseModel):
    recipient_id: int
    amount: float

class TransactionSchema(BaseModel):
    id: int
    sender_id: int
    recipient_id: int
    amount: float
    created_at: datetime



    class Config:
        orm_mode = True