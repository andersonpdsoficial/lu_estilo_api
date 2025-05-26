from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum
from pydantic import ConfigDict

class OrderStatus(str, Enum):
    pending = "pending"
    processing = "processing"
    shipped = "shipped"
    delivered = "delivered"
    canceled = "canceled"

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)

class OrderCreate(BaseModel):
    client_id: int
    items: List[OrderItemCreate]

class Order(OrderCreate):
    id: int
    user_id: int
    status: OrderStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)