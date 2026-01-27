from ollama import AsyncClient
import asyncio
from datetime import datetime
from utils import send_log
from translations import get_translation
from deep_translator import GoogleTranslator

client = AsyncClient()

async def translate_prompt(prompt, lang):
    if lang == "en":
        return prompt  # No need to translate if it's already in English
    try:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, lambda: GoogleTranslator(source='auto', target=lang).translate(prompt))
    except Exception as e:
        send_log(datetime.now(), f"Error translating prompt to {lang}: {e}")
        return prompt # Return original prompt on error

async def podcast_script(city, filtered_news_text, lang="es"):
    send_log(datetime.now(), f"Generating podcast script for city: {city} in {lang}.")

    if lang == "es":
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
    else:
        base_prompt = f"""
        You are Zarteando, a news podcast host.
        Your task is to create a short and engaging podcast script about today's news in {city}.
        The tone should be informal and friendly, as if you were talking to a friend.
        You can add your own personality, make subtle jokes, and offer brief opinions on the news.

        Here are the news stories to base your script on:
        {filtered_news_text}

        The user's language is:
        {lang}

        Structure your script as follows:
        1. A brief and catchy introduction. Mention the city you are talking about.
        2. Discuss the most interesting news. Summarize them in your own words.
        3. A brief conclusion to end the podcast.

        Guidelines:
        - The script must be for a single host (you, Zarteando).
        - Do not include any technical cues like "[MUSIC IN]" or "[SOUND EFFECT]".
        - The entire script must be a single block of text.
        - The podcast should last about 2-3 minutes, so keep the script concise.
        - The output should not contain any symbols other than punctuation.
        - No markdown language in the script.
        - The output must always be in the user's language. (Spanish or English es/en)
        """

    prompt = base_prompt if lang in ["es", "en"] else await translate_prompt(base_prompt, lang)

    try:
        response = await client.generate(
            model="gemma3:4b",
            prompt=prompt,
        )
        script = response.get("response", "")
        send_log(datetime.now(), f"Successfully generated podcast script for city: {city} in {lang}.")
        return script
    except Exception as e:
        send_log(datetime.now(), f"Error generating podcast script for city {city} in {lang}: {e}")
        return get_translation(lang, "error_generating_script", city=city)


async def daily_summary(city, news, lang="es"):
    send_log(datetime.now(), f"Generating daily summary for city: {city} in {lang}.")
    
    if lang == "es":
        base_prompt = f"Resume las noticias más importantes de hoy en {city}:\n{news}"
    else:
        base_prompt = f"Summarize today's most important news in {city}:\n{news}"

    prompt = base_prompt if lang in ["es", "en"] else await translate_prompt(base_prompt, lang)

    try:
        response = await client.generate(
            model="gemma3:4b",
            prompt=prompt,
        )
        summary = response.get("response", "")
        send_log(datetime.now(), f"Successfully generated daily summary for city: {city} in {lang}.")
        return summary
    except Exception as e:
        send_log(datetime.now(), f"Error generating daily summary for city {city} in {lang}: {e}")
        return get_translation(lang, "error_generating_summary", city=city)

async def select_and_adapt_news(city, news, user_interests, lang="es"):
    send_log(datetime.now(), f"Selecting and adapting news for city: {city} with interests: {user_interests} in {lang}.")
    
    news_block = "\n\n".join(
        f"NEWS {i+1}: Title: {n['title']}\nDescription: {n['description']}"
        for i, n in enumerate(news)
    )

    interests_text = ", ".join(user_interests)

    if lang == "es":
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
    else:
        base_prompt = f"""
        Your role is that of a news editor and podcast host.
        User profile:
        - City {city}
        - Main interests: {interests_text}
        Before generating it with the news below, you will have to filter among all the news received, by the user's tastes. Attention if there is nothing that matches, look for things
        moderately relevant to the topic. Always try to adapt to the user's tastes, if the news does not "cover", we will try to show other relevant news even if they do not have
        to do with the topic, but we will add "humor with user interests", and you will adapt the podcast to their preferences.

        Available news:
        {news_block}
        """

    prompt = base_prompt if lang in ["es", "en"] else await translate_prompt(base_prompt, lang)

    try:
        response = await client.generate(
            model="gemma3:4b",
            prompt=prompt
        )
        curated_news = response.get("response", "")
        send_log(datetime.now(), f"Successfully selected and adapted news for city: {city} in {lang}.")
        return curated_news
    except Exception as e:
        send_log(datetime.now(), f"Error selecting and adapting news for city {city} in {lang}: {e}")
        return get_translation(lang, "error_selecting_news", city=city)

async def daily_news_script(city, filtered_news_text, lang="es"):
    send_log(datetime.now(), f"Generating daily news script for city: {city} in {lang}.")

    if lang == "es":
        base_prompt = f"""
        Eres Zarteando, el presentador de tu resumen diario de noticias.
        Tu tarea es crear un guion breve y directo para el podcast diario programado sobre las noticias de hoy en {city}.
        El tono debe ser informativo pero cercano, ideal para alguien que escucha esto todos los días a la misma hora.

        Aquí están las noticias del día:
        {filtered_news_text}

        El idioma del usuario es:
        {lang}

        Estructura:
        1.  Saludo rápido ("Hola, aquí tienes tu dosis diaria de noticias para {city}...").
        2.  Resumen ágil de los puntos clave.
        3.  Despedida rápida hasta mañana.

        Directrices:
        - Sin indicaciones técnicas.
        - Un solo bloque de texto.
        - Duración: 1-2 minutos (más conciso que el podcast normal).
        - Output en el idioma del usuario.
        """
    else:
        base_prompt = f"""
        You are Zarteando, the host of your daily news summary.
        Your task is to create a brief and direct script for the scheduled daily podcast about today's news in {city}.
        The tone should be informative but close, ideal for someone who listens to this every day at the same time.

        Here are the news of the day:
        {filtered_news_text}

        The user's language is:
        {lang}

        Structure:
        1. Quick greeting ("Hello, here is your daily dose of news for {city}...").
        2. Agile summary of key points.
        3. Quick farewell until tomorrow.

        Guidelines:
        - No technical indications.
        - A single block of text.
        - Duration: 1-2 minutes (more concise than the normal podcast).
        - Output in the user's language.
        """

    prompt = base_prompt if lang in ["es", "en"] else await translate_prompt(base_prompt, lang)

    try:
        response = await client.generate(
            model="gemma3:4b",
            prompt=prompt,
        )
        script = response.get("response", "")
        send_log(datetime.now(), f"Successfully generated daily news script for city: {city} in {lang}.")
        return script
    except Exception as e:
        send_log(datetime.now(), f"Error generating daily news script for city {city} in {lang}: {e}")
        return get_translation(lang, "error_generating_script", city=city)