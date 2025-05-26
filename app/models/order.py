from sqlalchemy import Column, Integer, Enum, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.database import Base
import enum

class OrderStatus(str, enum.Enum):
    pending = "pending"
    processing = "processing"
    shipped = "shipped"
    delivered = "delivered"
    canceled = "canceled"

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    status = Column(Enum(OrderStatus), default=OrderStatus.pending, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    client = relationship("Client")
    user = relationship("User")
    items = relationship("OrderItem", back_populates="order")