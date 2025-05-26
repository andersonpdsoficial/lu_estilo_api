from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.whatsapp_message import WhatsAppMessage, MessageStatus
from app.models.client import Client
from app.schemas.whatsapp_message import WhatsAppMessageCreate
from app.database.database import get_db
from app.utils.whatsapp import send_whatsapp_message
from app.models.user import User
from app.utils.auth import get_current_user

router = APIRouter(prefix="/whatsapp", tags=["whatsapp"])

@router.post("/send", summary="Enviar mensagem WhatsApp", description="Envia uma mensagem WhatsApp para um cliente")
async def send_message(message: WhatsAppMessageCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    client = db.query(Client).filter(Client.id == message.client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    try:
        success = await send_whatsapp_message(client.phone, message.message)
        db_message = WhatsAppMessage(
            client_id=message.client_id,
            message=message.message,
            status=MessageStatus.sent if success else MessageStatus.failed
        )
        db.add(db_message)
        db.commit()
        db.refresh(db_message)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to send WhatsApp message")
        
        return {"message": "WhatsApp message sent"}
    except Exception as e:
        db_message = WhatsAppMessage(
            client_id=message.client_id,
            message=message.message,
            status=MessageStatus.failed
        )
        db.add(db_message)
        db.commit()
        raise HTTPException(status_code=500, detail=f"WhatsApp API error: {str(e)}")