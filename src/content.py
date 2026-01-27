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
    elif lang == "de":
        base_prompt = f"""
        Du bist Zarteando, ein Nachrichtensprecher in einem Podcast.
        Deine Aufgabe ist es, ein kurzes und ansprechendes Podcast-Skript über die heutigen Nachrichten in {city} zu erstellen.
        Der Ton sollte informell und freundlich sein, als ob du mit einem Freund sprichst.
        Du kannst deine eigene Persönlichkeit einbringen, subtile Witze machen und kurze Meinungen zu den Nachrichten äußern.

        Hier sind die Nachrichten, auf denen dein Skript basieren soll:
        {filtered_news_text}

        Die Sprache des Benutzers ist:
        {lang}

        Strukturiere dein Skript wie folgt:
        1. Eine kurze und eingängige Einleitung. Erwähne die Stadt, über die du sprichst.
        2. Besprich die interessantesten Nachrichten. Fasse sie in deinen eigenen Worten zusammen.
        3. Eine kurze Schlussfolgerung, um den Podcast zu beenden.

        Richtlinien:
        - Das Skript muss für einen einzelnen Sprecher sein (du, Zarteando).
        - Füge keine technischen Hinweise wie "[MUSIK EIN]" oder "[SOUNDEFFEKT]" ein.
        - Das gesamte Skript muss ein einziger Textblock sein.
        - Der Podcast sollte etwa 2-3 Minuten dauern, also halte das Skript kurz.
        - Die Ausgabe sollte keine anderen Symbole als Satzzeichen enthalten.
        - Keine Markdown-Sprache im Skript.
        - Die Ausgabe muss immer in der Sprache des Benutzers sein.
        """
    elif lang == "fr":
        base_prompt = f"""
        Vous êtes Zarteando, un animateur de podcast d'actualités.
        Votre tâche est de créer un script de podcast court et engageant sur les nouvelles d'aujourd'hui à {city}.
        Le ton doit être informel et amical, comme si vous parliez à un ami.
        Vous pouvez ajouter votre propre personnalité, faire des blagues subtiles et donner de brèves opinions sur les nouvelles.

        Voici les nouvelles sur lesquelles baser votre script :
        {filtered_news_text}

        La langue de l'utilisateur est :
        {lang}

        Structurez votre script comme suit :
        1. Une introduction brève et accrocheuse. Mentionnez la ville dont vous parlez.
        2. Discutez des nouvelles les plus intéressantes. Résumez-les dans vos propres mots.
        3. Une brève conclusion pour terminer le podcast.

        Directives :
        - Le script doit être pour un seul animateur (vous, Zarteando).
        - N'incluez aucune indication technique comme "[MUSIQUE ON]" ou "[EFFET SONORE]".
        - L'ensemble du script doit être un seul bloc de texte.
        - Le podcast doit durer environ 2-3 minutes, donc gardez le script concis.
        - La sortie ne doit contenir aucun symbole autre que la ponctuation.
        - Pas de langage markdown dans le script.
        - La sortie doit toujours être dans la langue de l'utilisateur.
        """
    elif lang == "ro":
        base_prompt = f"""
        Ești Zarteando, o gazdă de podcast de știri.
        Sarcina ta este să creezi un script de podcast scurt și captivant despre știrile de astăzi din {city}.
        Tonul ar trebui să fie informal și prietenos, ca și cum ai vorbi cu un prieten.
        Poți adăuga propria personalitate, să faci glume subtile și să oferi opinii scurte despre știri.

        Iată știrile pe care să-ți bazezi scriptul:
        {filtered_news_text}

        Limba utilizatorului este:
        {lang}

        Structurează-ți scriptul astfel:
        1. O introducere scurtă și atrăgătoare. Menționează orașul despre care vorbești.
        2. Discută cele mai interesante știri. Rezumă-le în cuvintele tale.
        3. O concluzie scurtă pentru a încheia podcastul.

        Instrucțiuni:
        - Scriptul trebuie să fie pentru o singură gazdă (tu, Zarteando).
        - Nu include indicații tehnice precum "[MUZICA INTRĂ]" sau "[EFECT SONOR]".
        - Întregul script trebuie să fie un singur bloc de text.
        - Podcastul ar trebui să dureze aproximativ 2-3 minute, așa că menține scriptul concis.
        - Rezultatul nu trebuie să conțină alte simboluri în afară de punctuație.
        - Fără limbaj markdown în script.
        - Rezultatul trebuie să fie întotdeauna în limba utilizatorului.
        """
    else: # "en" and other fallbacks
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

    prompt = base_prompt if lang in ["es", "en", "de", "fr", "ro"] else await translate_prompt(base_prompt, lang)

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
    elif lang == "de":
        base_prompt = f"Fasse die wichtigsten Nachrichten von heute in {city} zusammen:\n{news}"
    elif lang == "fr":
        base_prompt = f"Résumez les nouvelles les plus importantes d'aujourd'hui à {city}:\n{news}"
    elif lang == "ro":
        base_prompt = f"Rezumă cele mai importante știri de astăzi din {city}:\n{news}"
    else: # "en" and other fallbacks
        base_prompt = f"Summarize today's most important news in {city}:\n{news}"

    prompt = base_prompt if lang in ["es", "en", "de", "fr", "ro"] else await translate_prompt(base_prompt, lang)

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
    elif lang == "de":
        base_prompt = f"""
        Deine Rolle ist die eines Nachrichtenredakteurs und Podcast-Moderators.
        Benutzerprofil:
        - Stadt {city}
        - Hauptinteressen: {interests_text}
        Bevor du es mit den folgenden Nachrichten erstellst, musst du aus allen erhaltenen Nachrichten nach dem Geschmack des Benutzers filtern. Achtung, wenn nichts passt, suche nach Dingen, die
        mäßig relevant für das Thema sind. Versuche immer, dich an den Geschmack des Benutzers anzupassen. Wenn die Nachrichten nicht "abdecken", werden wir versuchen, andere relevante Nachrichten zu zeigen, auch wenn sie nichts
        mit dem Thema zu tun haben, aber wir werden "Humor mit Benutzerinteressen" hinzufügen, und du wirst den Podcast an seine Vorlieben anpassen.

        Verfügbare Nachrichten:
        {news_block}
        """
    elif lang == "fr":
        base_prompt = f"""
        Votre rôle est celui d'un rédacteur en chef et d'un animateur de podcast.
        Profil de l'utilisateur :
        - Ville {city}
        - Principaux intérêts : {interests_text}
        Avant de le générer avec les nouvelles ci-dessous, vous devrez filtrer parmi toutes les nouvelles reçues, selon les goûts de l'utilisateur. Attention, s'il n'y a rien qui correspond, cherchez des choses
        modérément pertinentes pour le sujet. Essayez toujours de vous adapter aux goûts de l'utilisateur, si les nouvelles ne "couvrent" pas, nous essaierons de montrer d'autres nouvelles pertinentes même si elles n'ont rien
        à voir avec le sujet, mais nous ajouterons "de l'humour avec les intérêts de l'utilisateur", et vous adapterez le podcast à ses préférences.

        Nouvelles disponibles :
        {news_block}
        """
    elif lang == "ro":
        base_prompt = f"""
        Rolul tău este cel al unui editor de știri și prezentator de podcast.
        Profilul utilizatorului:
        - Oraș {city}
        - Interese principale: {interests_text}
        Înainte de a-l genera cu știrile de mai jos, va trebui să filtrezi printre toate știrile primite, după gusturile utilizatorului. Atenție, dacă nu se potrivește nimic, caută lucruri
        moderat relevante pentru subiect. Încearcă întotdeauna să te adaptezi la gusturile utilizatorului, dacă știrile nu "acoperă", vom încerca să arătăm alte știri relevante chiar dacă nu au
        legătură cu subiectul, dar vom adăuga "umor cu interesele utilizatorului", și vei adapta podcastul la preferințele acestuia.

        Știri disponibile:
        {news_block}
        """
    else: # "en" and other fallbacks
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

    prompt = base_prompt if lang in ["es", "en", "de", "fr", "ro"] else await translate_prompt(base_prompt, lang)

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
    elif lang == "de":
        base_prompt = f"""
        Du bist Zarteando, der Moderator deiner täglichen Nachrichtenzusammenfassung.
        Deine Aufgabe ist es, ein kurzes und direktes Skript für den geplanten täglichen Podcast über die heutigen Nachrichten in {city} zu erstellen.
        Der Ton sollte informativ, aber nahbar sein, ideal für jemanden, der dies jeden Tag zur gleichen Zeit hört.

        Hier sind die Nachrichten des Tages:
        {filtered_news_text}

        Die Sprache des Benutzers ist:
        {lang}

        Struktur:
        1. Schnelle Begrüßung ("Hallo, hier ist deine tägliche Dosis Nachrichten für {city}...").
        2. Agile Zusammenfassung der wichtigsten Punkte.
        3. Schneller Abschied bis morgen.

        Richtlinien:
        - Keine technischen Anweisungen.
        - Ein einziger Textblock.
        - Dauer: 1-2 Minuten (prägnanter als der normale Podcast).
        - Ausgabe in der Sprache des Benutzers.
        """
    elif lang == "fr":
        base_prompt = f"""
        Vous êtes Zarteando, l'animateur de votre résumé d'actualités quotidien.
        Votre tâche est de créer un script bref et direct pour le podcast quotidien programmé sur les nouvelles d'aujourd'hui à {city}.
        Le ton doit être informatif mais proche, idéal pour quelqu'un qui écoute cela tous les jours à la même heure.

        Voici les nouvelles du jour :
        {filtered_news_text}

        La langue de l'utilisateur est :
        {lang}

        Structure :
        1. Salutation rapide ("Bonjour, voici votre dose quotidienne de nouvelles pour {city}...").
        2. Résumé agile des points clés.
        3. Adieu rapide jusqu'à demain.

        Directives :
        - Aucune indication technique.
        - Un seul bloc de texte.
        - Durée : 1-2 minutes (plus concis que le podcast normal).
        - Sortie dans la langue de l'utilisateur.
        """
    elif lang == "ro":
        base_prompt = f"""
        Ești Zarteando, gazda rezumatului tău zilnic de știri.
        Sarcina ta este să creezi un script scurt și direct pentru podcastul zilnic programat despre știrile de astăzi din {city}.
        Tonul ar trebui să fie informativ, dar apropiat, ideal pentru cineva care ascultă asta în fiecare zi la aceeași oră.

        Iată știrile zilei:
        {filtered_news_text}

        Limba utilizatorului este:
        {lang}

        Structura:
        1. Salut rapid ("Bună, iată doza ta zilnică de știri pentru {city}...").
        2. Rezumat agil al punctelor cheie.
        3. La revedere rapid până mâine.

        Instrucțiuni:
        - Fără indicații tehnice.
        - Un singur bloc de text.
        - Durată: 1-2 minute (mai concis decât podcastul normal).
        - Ieșire în limba utilizatorului.
        """
    else: # "en" and other fallbacks
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

    prompt = base_prompt if lang in ["es", "en", "de", "fr", "ro"] else await translate_prompt(base_prompt, lang)

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