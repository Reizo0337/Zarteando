import requests
import subprocess
import asyncio
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

def _generate_tts_sync(script, lang="es", output_path="output.ogg"):
    send_log(datetime.now(), "Generating audio from script.")

    try:
        # Select voice based on language
        voice_id = "es-ES-Javier"
        if lang == "en":
            voice_id = "en-US-Carter"
        elif lang == "de":
            voice_id = "de-DE-Bernd"
        elif lang == "fr":
            voice_id = "fr-FR-Antoine"
        elif lang == "ro":
            voice_id = "ro-RO-Andrei"

        # Generar audio en Murf (pidiendo OGG directamente)
        response = client.text_to_speech.generate(
            text=script,
            voice_id=voice_id,
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

async def generate_tts(script, lang="es", output_path="output.ogg"):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, _generate_tts_sync, script, lang, output_path)