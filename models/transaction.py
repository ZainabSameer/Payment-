from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import BaseModel

class TransactionModel(BaseModel):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    recipient_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    amount = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    sender = relationship("UserModel", foreign_keys=[sender_id])
    recipient = relationship("UserModel", foreign_keys=[recipient_id])

    