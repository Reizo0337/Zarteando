from openai import OpenAI
import uuid

client = OpenAI()

def text_to_audio(text):
    filename = f"podcast_{uuid.uuid4()}.mp3"
    with client.audio.speech.with_streaming_response.create(
        model = "gpt-4o-mini-tts",
        voice = "alloy",
        input = text
    ) as response:
        response.stream_to_file(filename)
    
    return filename