from pydantic import BaseModel
from enum import Enum
from datetime import datetime
from pydantic import ConfigDict

class MessageStatus(str, Enum):
    sent = "sent"
    failed = "failed"

class WhatsAppMessageCreate(BaseModel):
    client_id: int
    message: str

class WhatsAppMessage(WhatsAppMessageCreate):
    id: int
    sent_at: datetime
    status: MessageStatus

    model_config = ConfigDict(from_attributes=True)