from ollama import Client
from datetime import datetime
from utils import send_log
from translations import get_translation
from deep_translator import GoogleTranslator

client = Client()

def translate_prompt(prompt, lang):
    if lang == "en":
        return prompt  # No need to translate if it's already in English
    try:
        return GoogleTranslator(source='auto', target=lang).translate(prompt)
    except Exception as e:
        send_log(datetime.now(), f"Error translating prompt to {lang}: {e}")
        return prompt # Return original prompt on error

def podcast_script(city, filtered_news_text, lang="es"):
    send_log(datetime.now(), f"Generating podcast script for city: {city} in {lang}.")

    base_prompt = f"""
        Eres Zarteando, el presentador de un podcast de noticias.
        Tu tarea es crear un guion de podcast corto y atractivo sobre las noticias de hoy en {city}.
        El tono debe ser informal y amigable, como si estuvieras hablando con un amigo.
        Puedes añadir tu propia personalidad, hacer bromas sutiles y ofrecer breves opiniones sobre las noticias.

        Aquí están las noticias en las que debes basar tu guion:
        {filtered_news_text}

        El idioma del usuario es:
        {lang}

        Estructura tu guion de la siguiente manera:
        1.  Una introducción breve y pegadiza. Menciona la ciudad de la que estás hablando.
        2.  Comenta las noticias más interesantes. Resúmelas en tus propias palabras.
        3.  Una breve conclusión para terminar el podcast.

        Directrices:
        - El guion debe ser para un solo presentador (tú, Zarteando).
        - No incluyas ninguna indicación técnica como "[MÚSICA ENTRA]" o "[EFECTO DE SONIDO]".
        - El guion completo debe ser un único bloque de texto.
        - El podcast debe durar alrededor de 2-3 minutos, así que mantén el guion conciso.
        - El mensaje a recibir no tiene que tener ningun simbolo exceptuando los de puntuacion.
        - Nada de lenguaje markdown en el guion.
        - El output siempre tiene que tener el idioma del usuario. (Español o ingles es/en)
        """
    
    prompt = translate_prompt(base_prompt, lang)

    try:
        response = client.generate(
            model="gemma3:4b",
            prompt=prompt,
        )
        script = response.get("response", "")
        send_log(datetime.now(), f"Successfully generated podcast script for city: {city} in {lang}.")
        return script
    except Exception as e:
        send_log(datetime.now(), f"Error generating podcast script for city {city} in {lang}: {e}")
        return get_translation(lang, "error_generating_script", city=city)


def daily_summary(city, news, lang="es"):
    send_log(datetime.now(), f"Generating daily summary for city: {city} in {lang}.")
    
    base_prompt = f"Summarize today's most important news in {city}:\n{news}"
    prompt = translate_prompt(base_prompt, lang)

    try:
        response = client.generate(
            model="gemma3:4b",
            prompt=prompt,
        )
        summary = response.get("response", "")
        send_log(datetime.now(), f"Successfully generated daily summary for city: {city} in {lang}.")
        return summary
    except Exception as e:
        send_log(datetime.now(), f"Error generating daily summary for city {city} in {lang}: {e}")
        return get_translation(lang, "error_generating_summary", city=city)

def select_and_adapt_news(city, news, user_interests, lang="es"):
    send_log(datetime.now(), f"Selecting and adapting news for city: {city} with interests: {user_interests} in {lang}.")
    
    news_block = "\n\n".join(
        f"NEWS {i+1}: Title: {n['title']}\nDescription: {n['description']}"
        for i, n in enumerate(news)
    )

    interests_text = ", ".join(user_interests)

    base_prompt = f"""
        Tu rol es de un editor de noticias y presentador de podcast.
        Perfil del usuario:
        - Ciudad {city}
        - Intereses principales: {interests_text}
        Antes de generarlo con las noticias de abajo, vas a tener que filtrar entre todas las noticias recibidas, por los gustso del usuario. Atención si no hay nada que coincida, busca cosas
        medianamente relevantes con el tema. Siempre intenta adaptarte, a los gustos del usuario, si las noticias no "acaparan", intetaremos mostrar otras noticias relevantes aunque no tengan
        que ver con el tema, pero añadiremos "humor con intereses del usuario", y adaptaras el podcast a las preferencias de este.



        Noticias disponibles:
        {news_block}
        """
    
    prompt = translate_prompt(base_prompt, lang)

    try:
        response = client.generate(
            model="gemma3:4b",
            prompt=prompt
        )
        curated_news = response.get("response", "")
        send_log(datetime.now(), f"Successfully selected and adapted news for city: {city} in {lang}.")
        return curated_news
    except Exception as e:
        send_log(datetime.now(), f"Error selecting and adapting news for city {city} in {lang}: {e}")
        return get_translation(lang, "error_selecting_news", city=city)