from sqlalchemy import Column, Integer, String, Float, DateTime, ARRAY
from sqlalchemy.sql import func
from app.models.base import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False, index=True)
    price = Column(Float, nullable=False, index=True)
    barcode = Column(String, unique=True, index=True, nullable=False)
    section = Column(String, index=True, nullable=False)
    stock = Column(Integer, nullable=False)
    expiry_date = Column(DateTime, nullable=True, index=True)
    images = Column(ARRAY(String), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)