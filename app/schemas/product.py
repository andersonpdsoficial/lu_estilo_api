from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from pydantic import ConfigDict

class ProductBase(BaseModel):
    description: str
    price: float = Field(..., gt=0)
    barcode: str = Field(..., pattern=r'^\d{8,13}$')
    section: str
    stock: int = Field(..., ge=0)
    expiry_date: Optional[datetime] = None
    images: Optional[List[str]] = None

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)