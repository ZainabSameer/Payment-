from sqlalchemy import Column, Integer, String , DateTime
from sqlalchemy.orm import relationship
from .base import BaseModel
from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta
import jwt
from config.environment import secret
from datetime import datetime
from .base import Base  # Ensure you import your base class



class UserModel(BaseModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)  # Correctly defined
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    accounts = relationship("AccountModel", back_populates="user")  # Ensure it's plural

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