from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from .base import BaseModel
from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta
import jwt
from config.environment import secret

class UserModel(BaseModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)  

    
    accounts = relationship("AccountModel", back_populates="user")

    def set_password(self, password: str):
        self.password_hash = CryptContext(schemes=["bcrypt"]).hash(password)

    def verify_password(self, password: str) -> bool:
        return CryptContext(schemes=["bcrypt"]).verify(password, self.password_hash)

    def generate_token(self):
        payload = {
            "exp": datetime.now(timezone.utc) + timedelta(days=1),
            "iat": datetime.now(timezone.utc),
            "sub": str(self.id)
        }
        token = jwt.encode(payload, secret, algorithm="HS256")
        return token