from openai import OpenAI

client = OpenAI

def podcast_script(city, news, tiempo=5):
    news_text = "\n".join([f"{n['title']}: {n['description']}" for n in news])

    prompt = f"""
        Genera un guion de podcast de {tiempo} minutos sobre las noticias de hoy en {city}, 
        Estilo cercano y natural, como si estuvieras contandole a tu amigo / colega las noticias de hoy, algo parecido a la radio.
        Intentaremos, añadir alguna broma sutil con las noticias, entre noticia y noticia. O incluso dar opiniones sobre el tema en especifico.
        Tiene que ser entretenido. Tener una pequeña introduccion, como diciendo los titulos de las noticias.
        
        Estructura del guion:
        1. Introduccion
        2. Noticias
        3. Conclusion
        
        No te olvides nunca de eso. Tiene que ser lo más natural y gancho posible. No tiene que aburrir.
                
        Noticias:
        {news_text}
    """

    response = client.chat.completions.create(
        model="gpt-4-0-mini",
        messages=[{
            "role": "user",
            "content": prompt
        }]
    )

    return response.choices[0].message.content
    

def daily_summary(city, news):
    prompt = f"Resume las noticias más importantes de hoy en {city}:\n{news}"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content