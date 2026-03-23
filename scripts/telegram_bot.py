#Jesus Ariel Santos
#24-EISN-2-034 
import requests # Uso requests para enviar mensajes a través de la API de Telegram

# Token del bot de Telegram
TOKEN = "8638098308:AAHUaPz2p5rvH-NYr4M5xqgbPpVAKNRqs_g"

# ID del chat donde se enviarán los mensajes
CHAT_ID = "1091946866"

def enviar_alerta():
    # URL de la API de Telegram
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    # Mensaje que se enviará
    mensaje = "🚨 Alerta: Intruso detectado en la zona restringida"

    # Envío del mensaje
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": mensaje
    })