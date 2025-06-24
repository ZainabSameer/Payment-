from sqlalchemy import Column, Integer, Float, ForeignKey, String , Boolean
from sqlalchemy.orm import relationship
from .base import BaseModel

class AccountModel(BaseModel):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    #is_admin = Column(Boolean, nullable=False, default=False)

    balance = Column(Float, default=0.00)
    currency = Column(String(3), default="USD")

    user = relationship("UserModel", back_populates="accounts")  