from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from .user import UserResponseSchema
from decimal import Decimal
from datetime import datetime

class AccountSchema(BaseModel):
    id: Optional[int] = None
    user_id: int
    balance: Decimal
    currency: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class AccountCreate(BaseModel):
    user_id: int
    balance: Decimal
    currency: str

class AccountUpdate(BaseModel):
    balance: Optional[Decimal] = None
    currency: Optional[str] = None