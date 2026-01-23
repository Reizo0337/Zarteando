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
        Generate a podcast script about today's news in {city}.
        The style should be close and natural, as if you were telling a friend about the news.
        Add subtle jokes between news, or even give opinions on the topics.
        It has to be entertaining, with a short introduction mentioning the news headlines.
        Noticias:
        {filtered_news_text}
        Script structure:
        1. Introduction
        2. News
        3. Conclusion
        Estilo cercano y natural, como radio o nota de voz.
        Con introducción, desarrollo y cierre.
        Puedes opinar y hacer bromas sutiles.
        News:
        {filtered_news_text}
        Atencion:
        Lo tienes que hacer como si lo dices tu en primera persona, tu nombre va a ser Zarteando. Nada de ahora pausa, musica etc. Solo tu como si presentaras tu el podcast.
        No hagas intervenciones, el podcast es de 1-1. tu hablando al usuario. Nada de música efectos, de sonido etc. Solo el dialogo. No pongas como si fuera un dialogo, solo el texto
        que hay que leer nada mas. Ejemplo:
        Soy Zarteando, hoy os presento tal.
        ahora hablemos de la noticia x de la lista de noticias.
        Y sigues... No hace falta que pongas nada mas que lo que hay que leer sin nombres, etc.
        Your name is Zarteando. You are the host. Don't mention music or sound effects. Just the dialogue.
        The podcast is 1-on-1, you talking to the user.
        NO MAS DE 2 MINUTOS / 3 MINUTOS POR PODCAST.
        NO MORE THAN 2-3 MINUTES PER PODCAST.
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
        Tu rol es de un editor de noticias y presentador de podcast.w
        Perfil del usuario:
        - Ciudad {city}
        - Intereses principales: {interests_text}
        Antes de generarlo con las noticias de abajo, vas a tener que filtrar entre todas las noticias recibidas, por los gustso del usuario. Atención si no hay nada que coincida, busca cosas
        medianamente relevantes con el tema. Siempre intenta adaptarte, a los gustos del usuario, si las noticias no "acaparan", intetaremos mostrar otras noticias relevantes aunque no tengan
        que ver con el tema, pero añadiremos "humor con intereses del usuario", y adaptaras el podcast a las preferencias de este.

        Tarea:
        1. Lees todas las noticias.
        3. Descarta las que no encajan con sus intereses. (En caso de que no haya, no se descartan)
        4. Prioriza calidad y relevancia, no cantidad.
        5. Si una noticia encaja parcialmente, puedes adaptarla al interés del usuario. ATENCION SIN CAMBIAR O INVENTAR DATOS SOBRE LA NOTICIA.
        Devuelve el resultado como una lista ordenada de noticias seleccionadas,
        manteniendo título y una breve explicación de por qué es relevante.

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