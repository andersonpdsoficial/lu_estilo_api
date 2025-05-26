from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.database import Base
import enum

class MessageStatus(str, enum.Enum):
    sent = "sent"
    failed = "failed"

class WhatsAppMessage(Base):
    __tablename__ = "whatsapp_messages"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), index=True, nullable=False)
    message = Column(String, nullable=False)
    sent_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    status = Column(Enum(MessageStatus), default=MessageStatus.sent, nullable=False)

    client = relationship("Client")