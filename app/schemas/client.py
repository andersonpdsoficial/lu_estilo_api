from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from pydantic import ConfigDict

class ClientBase(BaseModel):
    name: str
    email: EmailStr
    cpf: str = Field(..., pattern=r'^\d{11}$')
    phone: str = Field(..., pattern=r'^\+?\d{10,15}$')

class ClientCreate(ClientBase):
    pass

class Client(ClientBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)