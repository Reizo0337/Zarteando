from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from news import get_news
from content import podcast_script
from tts import generate_tts as text_to_audio


# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Comandos disponibles: \n"
        "/start - Iniciar el bot \n"
        "/news - Mostrar noticias \n"
        "/podcast - Generar podcast \n"
        "/summary - Generar resumen \n"

        "/help - Mostrar esta ayuda \n"
    )

# /podcast <ciudad>
async def podcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usa: /podcast <ciudad>")
        return
    
    city = " ".join(context.args)
    await update.message.reply_text("Buscando noticias...")

    news = get_news(city, 5)
    if not news:
        await update.message.reply_text("No se encontraron noticias.")
        return
    
    script = podcast_script(city, news)
    await update.message.reply_text("Generando podcast...")

    audio_path = text_to_audio(script)
    await update.message.reply_audio(audio=open(audio_path, "rb"), title=f"Podcast de {city}")
    

app = ApplicationBuilder().token("8328525433:AAEoUO1Eqb9X0zD58SCTvuOH4eflT-8Cg_M").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("podcast", podcast))

app.run_polling()