from ollama import AsyncClient
from datetime import datetime
from utils import send_log
from translations import get_translation
client = AsyncClient(timeout=300)

async def podcast_script(city, filtered_news_text, lang="es"):
    send_log(datetime.now(), f"Generating podcast script for city: {city} in {lang}.")

    prompt = f"""
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

        Directrices tienes que tener esto en cuenta más que nada:
        - El guion debe ser para un solo presentador (tú, Zarteando).
        - No incluyas ninguna indicación técnica como "[MÚSICA ENTRA]" o "[EFECTO DE SONIDO]".
        - El guion completo debe ser un único bloque de texto.
        - El podcast debe durar alrededor de 2-3 minutos, así que mantén el guion conciso.
        - El mensaje a recibir no tiene que tener ningun simbolo exceptuando los de puntuacion.
        - IMPORTANTE: No uses formato Markdown (negritas, cursivas, encabezados). Solo texto plano.
        - Tienes que devolver solo el texto a leer, nada más.
        - El output siempre tiene que tener el idioma del usuario: {lang}.
        """

    try:
        client = AsyncClient(timeout=300)
        response = await client.generate(
            model="gemma3:4b",
            prompt=prompt,
            options={"num_ctx": 8192}
        )
        script = response.get("response", "")
        send_log(datetime.now(), f"Successfully generated podcast script for city: {city} in {lang}.")
        return script
    except Exception as e:
        send_log(datetime.now(), f"Error generating podcast script for city {city} in {lang}: {e}")
        return get_translation(lang, "error_generating_script", city=city)


async def daily_summary(city, news, lang="es"):
    send_log(datetime.now(), f"Generating daily summary for city: {city} in {lang}.")
    
    prompt = f"Resume las noticias más importantes de hoy en {city}. El output debe estar en {lang}. IMPORTANTE: No uses formato Markdown, solo texto plano:\n{news}"

    try:
        client = AsyncClient(timeout=300)
        response = await client.generate(
            model="gemma3:4b",
            prompt=prompt,
            options={"num_ctx": 8192}
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

    prompt = f"""
        Tu rol es de un editor de noticias y presentador de podcast.
        Perfil del usuario:
        - Ciudad {city}
        - Intereses principales: {interests_text}
        Antes de generarlo con las noticias de abajo, vas a tener que filtrar entre todas las noticias recibidas, por los gustos del usuario. Atención si no hay nada que coincida, busca cosas
        medianamente relevantes con el tema. Siempre intenta adaptarte, a los gustos del usuario, si las noticias no "acaparan", intentaremos mostrar otras noticias relevantes aunque no tengan
        que ver con el tema, pero añadiremos "humor con intereses del usuario", y adaptaras el podcast a las preferencias de este. No tienes que decir que no has encontrado noticias relevantes.


        Tu funcion es solo devolver las noticias de esa ciudad  con su titulo y contenido, nada más.
        IMPORTANTE: No uses formato Markdown.
        El idioma de salida debe ser: {lang}

        Noticias disponibles:
        {news_block}

        El formato del output debe ser:
        Noticia 1: TITULO, DESCRIPCION
        Noticia 2: TITULO, DESCRIPCION
        ...
        """

    try:
        client = AsyncClient(timeout=300)
        response = await client.generate(
            model="gemma3:4b",
            prompt=prompt,
            options={"num_ctx": 8192}
        )
        curated_news = response.get("response", "")
        send_log(datetime.now(), f"Successfully selected and adapted news for city: {city} in {lang}.")
        send_log(datetime.now(), f"Curated news: {curated_news}")
        return curated_news
    except Exception as e:
        send_log(datetime.now(), f"Error selecting and adapting news for city {city} in {lang}: {e}")
        return get_translation(lang, "error_selecting_news", city=city)

async def daily_news_script(city, filtered_news_text, lang="es"):
    send_log(datetime.now(), f"Generating daily news script for city: {city} in {lang}.")

    prompt = f"""
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
        - Debe ser para un solo presentador (tú, Zarteando).
        - El guion completo debe ser un único bloque de texto.
        - El podcast debe durar alrededor de 2-3 minutos, así que mantén el guion conciso.
        - El mensaje a recibir no tiene que tener ningun simbolo exceptuando los de puntuacion.
        - IMPORTANTE: No uses formato Markdown (negritas, cursivas, encabezados). Solo texto plano.
        - Tienes que devolver solo el texto a leer, nada más.
        - El output siempre tiene que tener el idioma del usuario:
        - Output en el idioma del usuario: {lang}.
        """

    try:
        client = AsyncClient(timeout=300)
        response = await client.generate(
            model="gemma3:4b",
            prompt=prompt,
            options={"num_ctx": 8192}
        )
        script = response.get("response", "")
        send_log(datetime.now(), f"Successfully generated daily news script for city: {city} in {lang}.")
        return script
    except Exception as e:
        send_log(datetime.now(), f"Error generating daily news script for city {city} in {lang}: {e}")
        return get_translation(lang, "error_generating_script", city=city)