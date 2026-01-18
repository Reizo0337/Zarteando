from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message_reply_text(
        "Comandos disponibles: \n"
        "/start - Iniciar el bot \n"
        "/news - Mostrar noticias \n"
        "/podcast - Generar podcast \n"
        "/summary - Generar resumen \n"

        "/help - Mostrar esta ayuda \n"
    )

app = ApplicationBuilder().token("8328525433:AAEoUO1Eqb9X0zD58SCTvuOH4eflT-8Cg_M").build()

app.add_handler(CommandHandler("start", start))
app.run_polling()