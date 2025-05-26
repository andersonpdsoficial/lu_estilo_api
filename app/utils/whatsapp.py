import aiohttp
from dotenv import load_dotenv
import os
import sentry_sdk

load_dotenv()

WHATSAPP_API_TOKEN = os.getenv("WHATSAPP_API_TOKEN")
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")

async def send_whatsapp_message(phone: str, message: str) -> bool:
    if not WHATSAPP_API_TOKEN or not WHATSAPP_PHONE_NUMBER_ID:
        sentry_sdk.capture_message("WhatsApp API credentials not configured")
        return False
    
    url = f"https://graph.facebook.com/v17.0/{WHATSAPP_PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_API_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "text",
        "text": {"body": message}
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as response:
                if response.status != 200:
                    error_text = await response.text()
                    sentry_sdk.capture_message(f"WhatsApp API error: {error_text}")
                    return False
                return True
    except Exception as e:
        sentry_sdk.capture_exception(e)
        return False