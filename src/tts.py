import os
import requests
from datetime import datetime
from utils import send_log

# Carga la API Key del archivo .env
ELEVEN_API_KEY = "sk_179b1beaac8b47ff793a4600505462f9b2f8d79e2ec385da"

if not ELEVEN_API_KEY:
    send_log(datetime.now(), "CRITICAL: ElevenLabs API Key not found.")

VOICE_ID = "851ejYcv2BoNPjrkw93G" 
MODEL_ID = "eleven_multilingual_v2"


def generate_tts(text: str, output_file: str = "data/podcast.ogg") -> str:
    send_log(datetime.now(), f"Generating TTS for text (first 50 chars): '{text[:50]}...'.")
    
    if not ELEVEN_API_KEY:
        send_log(datetime.now(), "Cannot generate TTS: ElevenLabs API Key is missing.")
        return ""

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVEN_API_KEY
    }

    payload = {
        "text": text,
        "model_id": MODEL_ID,
        "voice_settings": {
            "stability": 0.5,         # control de consistencia de la voz
            "similarity_boost": 0.5  
        }
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Lanza error si falla la petición
    except requests.exceptions.RequestException as e:
        send_log(datetime.now(), f"Error generating TTS: {e}")
        return ""

    # Ensure data directory exists
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Guarda el audio en un archivo
    try:
        with open(output_file, "wb") as f:
            f.write(response.content)
        
        send_log(datetime.now(), f"TTS audio generated successfully at: {output_file}")
        return output_file
    except IOError as e:
        send_log(datetime.now(), f"Error saving TTS audio file to {output_file}: {e}")
        return ""