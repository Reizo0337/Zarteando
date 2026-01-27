import os
import asyncio
from content import client
from news import get_news
from tts import generate_tts as text_to_audio

async def run_diagnostics():
    """Runs all diagnostic checks and returns a list of results."""
    results = []
    # 1. Check Ollama
    try:
        await client.list()
        results.append("✅ Servicio Ollama iniciado correctamente.")
    except Exception as e:
        results.append(f"❌ Servicio Ollama falló: {e}")

    # 2. Check GNews
    try:
        # Attempt to fetch news for a generic topic to verify API/Library
        await get_news("Technology", lang="en")
        results.append("✅ Servicio GNews iniciado correctamente.")
    except Exception as e:
        results.append(f"❌ Servicio GNews falló: {e}")

    # 3. Check TTS
    try:
        # Generate a short test audio
        path = await text_to_audio("Test system check.", lang="es")
        if path and os.path.exists(path):
            results.append("✅ Servicio TTS iniciado correctamente.")
            # Clean up the test file
            try:
                os.remove(path)
            except OSError:
                pass
        else:
            results.append("❌ Servicio TTS falló: No se generó archivo.")
    except Exception as e:
        results.append(f"❌ Servicio TTS falló: {e}")
    return results

def print_diagnostics():
    """Runs diagnostics and prints the results to stdout."""
    print("🔄 Verificando servicios...")
    results = asyncio.run(run_diagnostics())
    for line in results:
        print(line)