import os
import requests

# Carga la API Key del archivo .env
ELEVEN_API_KEY = "sk_179b1beaac8b47ff793a4600505462f9b2f8d79e2ec385da"

if not ELEVEN_API_KEY:
    raise ValueError("No se encontró la API Key de ElevenLabs. Ponla en el archivo .env como ELEVENLABS_API_KEY.")

VOICE_ID = "851ejYcv2BoNPjrkw93G" 
MODEL_ID = "eleven_multilingual_v2"


def generate_tts(text: str, output_file: str = "podcast.ogg") -> str:
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
            "similarity_boost": 0.5    # cuánto se parece al modelo original
        }
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Lanza error si falla la petición
    except requests.exceptions.RequestException as e:
        print(f"Error generando TTS: {e}")
        return ""

    # Guarda el audio en un archivo
    with open(output_file, "wb") as f:
        f.write(response.content)

    print(f"[TTS] Audio generado correctamente en: {output_file}")
    return output_file