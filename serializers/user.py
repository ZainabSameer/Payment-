from pydantic import BaseModel , ConfigDict
from typing import Optional
from datetime import datetime



class UserSchema(BaseModel):
    #id: int
    username: str
    email: str
    password:str
    #is_admin: Optional[bool] = False
    created_at: datetime
    updated_at: Optional[datetime] = None


    class Config:
        orm_mode = True

class UserResponseSchema(BaseModel):
    username: str
    email: str

class UserLogin(BaseModel):
    username: str
    password: str  
class UserToken(BaseModel):
    token: str
    message: str

    model_config = ConfigDict(
        from_attributes=True  
    )
