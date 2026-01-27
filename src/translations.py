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
        "welcome_message": "👋 ¡Bienvenido a NewsPodBot!\n\nVamos a configurar tu perfil para darte las mejores noticias.\n\nPrimero, selecciona tu idioma:",
        "lets_configure_interests": "✅ Idioma guardado.\n\nAhora selecciona tus temas de interés para personalizar las noticias:",
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
        "welcome_message": "👋 Welcome to NewsPodBot!\n\nLet's set up your profile to get the best news.\n\nFirst, select your language:",
        "lets_configure_interests": "✅ Language saved.\n\nNow select your interests to customize the news:",
        "setup_complete": "✅ Setup complete!\n\nYou can now use /podcast <city> to listen to the news."
    }
}

def get_translation(lang, key, **kwargs):
    """
    Retrieves a translated string for a given language and key.
    """
    return TRANSLATIONS.get(lang, TRANSLATIONS["es"]).get(key, key).format(**kwargs)
