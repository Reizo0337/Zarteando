from ollama import Client
from datetime import datetime
from utils import send_log

client = Client()


def podcast_script(city, filtered_news_text):
    send_log(datetime.now(), f"Generating podcast script for city: {city}.")
    prompt = f"""
        Genera un guion de podcast sobre las noticias de hoy en {city}, 
        estilo cercano y natural, como si estuvieras contándole a tu amigo/ colega las noticias de hoy, algo parecido a la radio.
        Añade alguna broma sutil entre noticias, o incluso da opiniones sobre los temas.
        Tiene que ser entretenido, con una pequeña introducción como diciendo los títulos de las noticias.

        Estructura del guion:
        1. Introducción
        2. Noticias
        3. Conclusión

        Noticias:
        {filtered_news_text}

        Estilo cercano y natural, como radio o nota de voz.
        Con introducción, desarrollo y cierre.
        Puedes opinar y hacer bromas sutiles.

        Atencion:
        Lo tienes que hacer como si lo dices tu en primera persona, tu nombre va a ser Zarteando. Nada de ahora pausa, musica etc. Solo tu como si presentaras tu el podcast.
        No hagas intervenciones, el podcast es de 1-1. tu hablando al usuario. Nada de música efectos, de sonido etc. Solo el dialogo. No pongas como si fuera un dialogo, solo el texto
        que hay que leer nada mas. Ejemplo:
        Soy Zarteando, hoy os presento tal.
        ahora hablemos de la noticia x de la lista de noticias.
        Y sigues... No hace falta que pongas nada mas que lo que hay que leer sin nombres, etc.

        NO MAS DE 2 MINUTOS / 3 MINUTOS POR PODCAST.
        """
    try:
        response = client.generate(
            model="gemma3:4b",
            prompt=prompt,
        )
        script = response.get("response", "")
        send_log(datetime.now(), f"Successfully generated podcast script for city: {city}.")
        send_log(datetime.now(), f"AI RESPONSE (PODCAST SCRIPT for {city}): {script[:100]}...")
        return script
    except Exception as e:
        send_log(datetime.now(), f"Error generating podcast script for city {city}: {e}")
        return f"Error al generar el guion para {city}."


def daily_summary(city, news):
    send_log(datetime.now(), f"Generating daily summary for city: {city}.")
    prompt = f"Resume las noticias más importantes de hoy en {city}:\n{news}"

    try:
        response = client.generate(
            model="gemma3:4b",
            prompt=prompt,
        )
        summary = response.get("response", "")
        send_log(datetime.now(), f"Successfully generated daily summary for city: {city}.")
        send_log(datetime.now(), f"AI RESPONSE (DAILY SUMMARY for {city}): {summary[:100]}...")
        return summary
    except Exception as e:
        send_log(datetime.now(), f"Error generating daily summary for city {city}: {e}")
        return f"Error al generar el resumen para {city}."

def select_and_adapt_news(city, news, user_interests):
    send_log(datetime.now(), f"Selecting and adapting news for city: {city} with interests: {user_interests}.")
    news_block = "\n\n".join(
        f"NOTICIA {i+1}: Titulo: {n['title']}\nDescripcion: {n['description']}"
        for i, n in enumerate(news)
    )

    interests_text = ", ".join(user_interests)

    prompt = f"""
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
    try:
        response = client.generate(
            model="gemma3:4b",
            prompt=prompt
        )
        curated_news = response.get("response", "")
        send_log(datetime.now(), f"Successfully selected and adapted news for city: {city}.")
        send_log(datetime.now(), f"AI RESPONSE (CURATED NEWS for {city}): {curated_news[:100]}...")
        return curated_news
    except Exception as e:
        send_log(datetime.now(), f"Error selecting and adapting news for city {city}: {e}")
        return f"Error al seleccionar las noticias para {city}."