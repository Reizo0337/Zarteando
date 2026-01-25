import requests
import subprocess
from datetime import datetime
from utils import send_log
from murf import Murf
import os
from dotenv import load_dotenv

load_dotenv()

MURF_KEY = os.getenv("MURF_API_KEY")

client = Murf(
    api_key=MURF_KEY,
)

def generate_tts(script, output_path="output.ogg"):
    send_log(datetime.now(), "Generating audio from script.")

    try:
        # Generar audio en Murf (pidiendo OGG directamente)
        response = client.text_to_speech.generate(
            text=script,
            voice_id="es-ES-Javier",
            format="OGG"  # 🔥 así evitas convertir después
        )

        # Obtener URL correcta del SDK
        audio_url = getattr(response, "audio_file", None)

        if not audio_url:
            send_log(datetime.now(), f"No audio URL found. Full response: {response}")
            return None

        # Descargar audio
        r = requests.get(audio_url, timeout=30)
        r.raise_for_status()

        with open(output_path, "wb") as f:
            f.write(r.content)

        send_log(datetime.now(), f"Audio generated at {output_path}")
        return output_path

    except Exception as e:
        send_log(datetime.now(), f"Error generating audio: {e}")
        return None