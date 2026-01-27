# translations.py

TRANSLATIONS = {
    "es": {
        "help_message": "Comandos disponibles: \n"
                        "/podcast <ciudad> - Crea un podcast de las noticias de tu ciudad.\n"
                        "/resumen - Generamos un resumen de las noticias más importantes de hoy. \n"
                        "/dailynews <ciudad> <hora> - Programar un podcast diario. \n"
                        "/stopdailynews <ciudad> - Desactivar un podcast diario. \n"
                        "/configure - Configurar el bot. \n"
                        "/language - Cambiar el idioma del bot. \n"
                        "/help - Mostrar comandos disponibles. \n",
        "podcast_usage": "Usa: /podcast <ciudad>",
        "summary_usage": "Usa: /resumen <ciudad>",
        "dailynews_usage": "Usa: /dailynews <ciudad> <hora>",
        "dailynews_scheduled": "✅ Podcast programado para {city} a las {time} diariamente.",
        "stopdailynews_usage": "Usa: /stopdailynews <ciudad>",
        "stopdailynews_success": "✅ Podcast diario para {city} desactivado.",
        "stopdailynews_not_found": "❌ No se encontró ningún podcast programado para {city}.",
        "searching_news": "📰 Buscando noticias...",
        "no_news_found": "❌ No se encontraron noticias.",
        "selecting_news": "🧠 Seleccionando noticias para ti...",
        "generating_script": "🎙️ Generando guion...",
        "error_generating_audio": "❌ Error al generar el audio.",
        "podcast_caption": "🎧 Podcast de {city}",
        "generating_summary": "📄 Generando resumen...",
        "interests_config": "Configura tus intereses: ",
        "interests_saved": "✅ Intereses guardados:\n\n",
        "language_config": "Cambiar el idioma del bot: ",
        "language_saved": "Idioma cambiado a {language_name}",
        "save": "💾 Guardar",
        "error_generating_script": "Error al generar el guion para {city}.",
        "error_selecting_news": "Error al seleccionar las noticias para {city}.",
        "error_generating_summary": "Error al generar el resumen para {city}.",
        "welcome_message": "👋 ¡Bienvenido a NewsPodBot!\n\n"
                         "Vamos a configurar tu perfil para darte las mejores noticias.\n\n"
                         "Primero, selecciona tu idioma:",
        "lets_configure_interests": "✅ Idioma guardado.\n\nAhora selecciona tus temas de interés para personalizar las noticias:",
        "interests": {
            "politica": "Política",
            "economia": "Economía",
            "tecnologia": "Tecnología",
            "deportes": "Deportes",
            "cultura": "Cultura",
            "sociedad": "Sociedad",
            "ciencia": "Ciencia",
            "salud": "Salud"
        },
        "setup_complete": "✅ ¡Configuración completa!\n\nYa puedes usar /podcast <ciudad> para escuchar las noticias."
    },
    "en": {
        "help_message": "Available commands: \n"
                        "/podcast <city> - Create a podcast of the news in your city.\n"
                        "/summary - We generate a summary of today's most important news. \n"
                        "/dailynews <city> <time> - Schedule a daily podcast. \n"
                        "/stopdailynews <city> - Stop a daily podcast. \n"
                        "/configure - Configure the bot. \n"
                        "/language - Change the bot's language. \n"
                        "/help - Show available commands. \n",
        "podcast_usage": "Usage: /podcast <city>",
        "summary_usage": "Usage: /summary <city>",
        "dailynews_usage": "Usage: /dailynews <city> <time>",
        "dailynews_scheduled": "✅ Daily podcast scheduled for {city} at {time}.",
        "stopdailynews_usage": "Usage: /stopdailynews <city>",
        "stopdailynews_success": "✅ Daily podcast for {city} deactivated.",
        "stopdailynews_not_found": "❌ No scheduled podcast found for {city}.",
        "searching_news": "📰 Searching for news...",
        "no_news_found": "❌ No news found.",
        "selecting_news": "🧠 Selecting news for you...",
        "generating_script": "🎙️ Generating script...",
        "error_generating_audio": "❌ Error generating audio.",
        "podcast_caption": "🎧 Podcast from {city}",
        "generating_summary": "📄 Generating summary...",
        "interests_config": "Set your interests: ",
        "interests_saved": "✅ Interests saved:\n\n",
        "language_config": "Change bot language: ",
        "language_saved": "Language set to {language_name}",
        "save": "💾 Save",
        "error_generating_script": "Error generating script for {city}.",
        "error_selecting_news": "Error selecting news for {city}.",
        "error_generating_summary": "Error generating summary for {city}.",
        "welcome_message": "👋 Welcome to NewsPodBot!\n\n"
                         "Let's set up your profile to get the best news.\n\n"
                         "First, select your language:",
        "lets_configure_interests": "✅ Language saved.\n\nNow select your interests to customize the news:",
        "interests": {
            "politica": "Politics",
            "economia": "Economy",
            "tecnologia": "Technology",
            "deportes": "Sports",
            "cultura": "Culture",
            "sociedad": "Society",
            "ciencia": "Science",
            "salud": "Health"
        },
        "setup_complete": "✅ Setup complete!\n\nYou can now use /podcast <city> to listen to the news."
    },
    "de": {
        "help_message": "Verfügbare Befehle: \n"
                        "/podcast <Stadt> - Erstellt einen Podcast mit den Nachrichten aus deiner Stadt.\n"
                        "/resumen - Wir erstellen eine Zusammenfassung der wichtigsten Nachrichten von heute. \n"
                        "/dailynews <Stadt> <Uhrzeit> - Einen täglichen Podcast planen. \n"
                        "/stopdailynews <Stadt> - Einen täglichen Podcast beenden. \n"
                        "/configure - Den Bot konfigurieren. \n"
                        "/language - Die Sprache des Bots ändern. \n"
                        "/help - Verfügbare Befehle anzeigen. \n",
        "podcast_usage": "Benutzung: /podcast <Stadt>",
        "summary_usage": "Benutzung: /resumen <Stadt>",
        "dailynews_usage": "Benutzung: /dailynews <Stadt> <Uhrzeit>",
        "dailynews_scheduled": "✅ Täglicher Podcast für {city} um {time} Uhr geplant.",
        "stopdailynews_usage": "Benutzung: /stopdailynews <Stadt>",
        "stopdailynews_success": "✅ Täglicher Podcast für {city} deaktiviert.",
        "stopdailynews_not_found": "❌ Kein geplanter Podcast für {city} gefunden.",
        "searching_news": "📰 Suche nach Nachrichten...",
        "no_news_found": "❌ Keine Nachrichten gefunden.",
        "selecting_news": "🧠 Wähle Nachrichten für dich aus...",
        "generating_script": "🎙️ Skript wird generiert...",
        "error_generating_audio": "❌ Fehler beim Erzeugen der Audiodatei.",
        "podcast_caption": "🎧 Podcast aus {city}",
        "generating_summary": "📄 Zusammenfassung wird erstellt...",
        "interests_config": "Stelle deine Interessen ein: ",
        "interests_saved": "✅ Interessen gespeichert:\n\n",
        "language_config": "Sprache des Bots ändern: ",
        "language_saved": "Sprache auf {language_name} geändert",
        "save": "💾 Speichern",
        "error_generating_script": "Fehler beim Erstellen des Skripts für {city}.",
        "error_selecting_news": "Fehler bei der Auswahl der Nachrichten für {city}.",
        "error_generating_summary": "Fehler beim Erstellen der Zusammenfassung für {city}.",
        "welcome_message": "👋 Willkommen bei NewsPodBot!\n\n"
                         "Lass uns dein Profil einrichten, um dir die besten Nachrichten zu liefern.\n\n"
                         "Zuerst, wähle deine Sprache:",
        "lets_configure_interests": "✅ Sprache gespeichert.\n\nWähle nun deine Interessen aus, um die Nachrichten zu personalisieren:",
        "interests": {
            "politica": "Politik",
            "economia": "Wirtschaft",
            "tecnologia": "Technologie",
            "deportes": "Sport",
            "cultura": "Kultur",
            "sociedad": "Gesellschaft",
            "ciencia": "Wissenschaft",
            "salud": "Gesundheit"
        },
        "setup_complete": "✅ Einrichtung abgeschlossen!\n\nDu kannst jetzt /podcast <Stadt> verwenden, um die Nachrichten anzuhören."
    },
    "fr": {
        "help_message": "Commandes disponibles : \n"
                        "/podcast <ville> - Crée un podcast des nouvelles de ta ville.\n"
                        "/resumen - Nous générons un résumé des nouvelles les plus importantes d'aujourd'hui. \n"
                        "/dailynews <ville> <heure> - Planifier un podcast quotidien. \n"
                        "/stopdailynews <ville> - Arrêter un podcast quotidien. \n"
                        "/configure - Configurer le bot. \n"
                        "/language - Changer la langue du bot. \n"
                        "/help - Afficher les commandes disponibles. \n",
        "podcast_usage": "Utilisation : /podcast <ville>",
        "summary_usage": "Utilisation : /resumen <ville>",
        "dailynews_usage": "Utilisation : /dailynews <ville> <heure>",
        "dailynews_scheduled": "✅ Podcast quotidien planifié pour {city} à {time}.",
        "stopdailynews_usage": "Utilisation : /stopdailynews <ville>",
        "stopdailynews_success": "✅ Podcast quotidien pour {city} désactivé.",
        "stopdailynews_not_found": "❌ Aucun podcast planifié trouvé pour {city}.",
        "searching_news": "📰 Recherche de nouvelles...",
        "no_news_found": "❌ Aucune nouvelle trouvée.",
        "selecting_news": "🧠 Sélection des nouvelles pour toi...",
        "generating_script": "🎙️ Génération du script...",
        "error_generating_audio": "❌ Erreur lors de la génération de l'audio.",
        "podcast_caption": "🎧 Podcast de {city}",
        "generating_summary": "📄 Génération du résumé...",
        "interests_config": "Configure tes centres d'intérêt : ",
        "interests_saved": "✅ Centres d'intérêt sauvegardés :\n\n",
        "language_config": "Changer la langue du bot : ",
        "language_saved": "Langue définie sur {language_name}",
        "save": "💾 Enregistrer",
        "error_generating_script": "Erreur lors de la génération du script pour {city}.",
        "error_selecting_news": "Erreur lors de la sélection des nouvelles pour {city}.",
        "error_generating_summary": "Erreur lors de la génération du résumé pour {city}.",
        "welcome_message": "👋 Bienvenue sur NewsPodBot !\n\n"
                         "Configurons ton profil pour obtenir les meilleures nouvelles.\n\n"
                         "Tout d'abord, sélectionne ta langue :",
        "lets_configure_interests": "✅ Langue enregistrée.\n\nMaintenant, sélectionne tes centres d'intérêt pour personnaliser les nouvelles :",
        "interests": {
            "politica": "Politique",
            "economia": "Économie",
            "tecnologia": "Technologie",
            "deportes": "Sports",
            "cultura": "Culture",
            "sociedad": "Société",
            "ciencia": "Science",
            "salud": "Santé"
        },
        "setup_complete": "✅ Configuration terminée !\n\nTu peux maintenant utiliser /podcast <ville> pour écouter les nouvelles."
    },
    "ro": {
        "help_message": "Comenzi disponibile: \n"
                        "/podcast <oraș> - Creează un podcast cu știrile din orașul tău.\n"
                        "/resumen - Generăm un rezumat al celor mai importante știri de astăzi. \n"
                        "/dailynews <oraș> <ora> - Programează un podcast zilnic. \n"
                        "/stopdailynews <oraș> - Oprește un podcast zilnic. \n"
                        "/configure - Configurează bot-ul. \n"
                        "/language - Schimbă limba bot-ului. \n"
                        "/help - Afișează comenzile disponibile. \n",
        "podcast_usage": "Utilizare: /podcast <oraș>",
        "summary_usage": "Utilizare: /resumen <oraș>",
        "dailynews_usage": "Utilizare: /dailynews <oraș> <ora>",
        "dailynews_scheduled": "✅ Podcast zilnic programat pentru {city} la {time}.",
        "stopdailynews_usage": "Utilizare: /stopdailynews <oraș>",
        "stopdailynews_success": "✅ Podcast-ul zilnic pentru {city} a fost dezactivat.",
        "stopdailynews_not_found": "❌ Nu a fost găsit niciun podcast programat pentru {city}.",
        "searching_news": "📰 Se caută știri...",
        "no_news_found": "❌ Nu s-au găsit știri.",
        "selecting_news": "🧠 Se selectează știri pentru tine...",
        "generating_script": "🎙️ Se generează scriptul...",
        "error_generating_audio": "❌ Eroare la generarea audio.",
        "podcast_caption": "🎧 Podcast din {city}",
        "generating_summary": "📄 Se generează rezumatul...",
        "interests_config": "Setează-ți interesele: ",
        "interests_saved": "✅ Interese salvate:\n\n",
        "language_config": "Schimbă limba bot-ului: ",
        "language_saved": "Limba setată la {language_name}",
        "save": "💾 Salvează",
        "error_generating_script": "Eroare la generarea scriptului pentru {city}.",
        "error_selecting_news": "Eroare la selectarea știrilor pentru {city}.",
        "error_generating_summary": "Eroare la generarea rezumatului pentru {city}.",
        "welcome_message": "👋 Bun venit la NewsPodBot!\n\n"
                         "Să-ți configurăm profilul pentru a primi cele mai bune știri.\n\n"
                         "Mai întâi, selectează-ți limba:",
        "lets_configure_interests": "✅ Limba salvată.\n\nAcum selectează-ți interesele pentru a personaliza știrile:",
        "interests": {
            "politica": "Politică",
            "economia": "Economie",
            "tecnologia": "Tehnologie",
            "deportes": "Sport",
            "cultura": "Cultură",
            "sociedad": "Societate",
            "ciencia": "Știință",
            "salud": "Sănătate"
        },
        "setup_complete": "✅ Configurare finalizată!\n\nAcum poți folosi /podcast <oraș> pentru a asculta știrile."
    }
}

def get_translation(lang, key, **kwargs):
    translation_table = TRANSLATIONS.get(lang, TRANSLATIONS["es"])
    translation = translation_table.get(key, key)
    
    if kwargs and isinstance(translation, str):
        return translation.format(**kwargs)
    return translation
