from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from pydantic import ConfigDict
from app.models.user import UserRole

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    role: UserRole = UserRole.user

class User(UserBase):
    id: int
    role: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str