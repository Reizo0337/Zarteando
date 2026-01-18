from ollama import Client

client = Client()


def podcast_script(city, news, tiempo=5):
    news_text = "\n".join([f"{n['title']}: {n['description']}" for n in news])

    prompt = f"""
        Genera un guion de podcast de {tiempo} minutos sobre las noticias de hoy en {city}, 
        estilo cercano y natural, como si estuvieras contándole a tu amigo/ colega las noticias de hoy, algo parecido a la radio.
        Añade alguna broma sutil entre noticias, o incluso da opiniones sobre los temas.
        Tiene que ser entretenido, con una pequeña introducción como diciendo los títulos de las noticias.

        Estructura del guion:
        1. Introducción
        2. Noticias
        3. Conclusión

        Noticias:
        {news_text}

        Atencion:
        Lo tienes que hacer como si lo dices tu en primera persona, tu nombre va a ser Zarteando. Nada de ahora pausa, musica etc. Solo tu como si presentaras tu el podcast.
        No hagas intervenciones, el podcast es de 1-1. tu hablando al usuario. Nada de música efectos, de sonido etc. Solo el dialogo. No pongas como si fuera un dialogo, solo el texto
        que hay que leer nada mas. Ejemplo:
        Soy Zarteando, hoy os presento tal.
        ahora hablemos de la noticia x de la lista de noticias.
        Y sigues... No hace falta que pongas nada mas que lo que hay que leer sin nombres, etc.
        """

    response = client.generate(
        model="gemma3:4b",
        prompt=prompt,
    )

    print("AI RESPONSE (PODCAST SCRIPT):", response.response)

    # Accede al texto correctamente
    return response.response


def daily_summary(city, news):

    prompt = f"Resume las noticias más importantes de hoy en {city}:\n{news}"

    response = client.generate(
        model="gemma3:4b",
        prompt=prompt,
    )

    print("AI RESPONSE (PODCAST SCRIPT):", response.response)

    return response.response
