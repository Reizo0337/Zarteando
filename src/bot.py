from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

from news import get_news
from content import podcast_script, select_and_adapt_news
from tts import generate_tts as text_to_audio
from profile import set_users_interests, get_user_profile

from config import AVAILABLE_INTERESTS
from utils import send_log

# /start
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    send_log(datetime.now(), f"User {user_id} requested help.")
    await update.message.reply_text(
        "Comandos disponibles: \n"
        "/podcast <ciudad> - Crea un podcast de las noticias de tu ciudad.\n"
        "/resumen - Generamos un resumen de las noticias más importantes de hoy. \n"
        "/configure - Configurar el bot. \n"
        "/help - Mostrar comandos disponibles. \n"
    )

# /podcast <ciudad>
async def podcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    send_log(datetime.now(), f"User {user_id} requested a podcast.")
    if not context.args:
        send_log(datetime.now(), f"User {user_id} did not provide a city for the podcast.")
        await update.message.reply_text("Usa: /podcast <ciudad>")
        return

    city = " ".join(context.args)
    send_log(datetime.now(), f"User {user_id} requested a podcast for city: {city}.")

    await update.message.chat.send_action(action="typing")
    await update.message.reply_text("📰 Buscando noticias...")

    news = get_news(city)
    if not news:
        send_log(datetime.now(), f"No news found for city: {city}.")
        await update.message.reply_text("❌ No se encontraron noticias.")
        return
    
    send_log(datetime.now(), f"Found {len(news)} news articles for city: {city}.")

    # 🧠 Obtener preferencias del usuario
    profile = get_user_profile(user_id)
    user_preferences = profile["interests"] if profile and "interests" in profile else []
    send_log(datetime.now(), f"User {user_id} has interests: {user_preferences}.")

    await update.message.chat.send_action(action="typing")
    await update.message.reply_text("🧠 Seleccionando noticias para ti...")

    curated_news = select_and_adapt_news(
        city=city,
        news=news,
        user_interests=user_preferences
    )
    send_log(datetime.now(), f"Curated {len(curated_news)} news articles for user {user_id}.")

    await update.message.chat.send_action(action="typing")
    await update.message.reply_text("🎙️ Generando guion...")

    script = podcast_script(city, curated_news)
    send_log(datetime.now(), f"Generated podcast script for user {user_id}.")

    # Simula grabación
    await update.message.chat.send_action(action="record_audio")

    audio_path = text_to_audio(script)  # debe devolver .ogg
    if not audio_path:
        send_log(datetime.now(), f"Error generating audio for user {user_id}.")
        await update.message.reply_text("❌ Error al generar el audio.")
        return
        
    send_log(datetime.now(), f"Generated audio at {audio_path} for user {user_id}.")

    with open(audio_path, "rb") as audio:
        await update.message.reply_voice(
            voice=audio,
            caption=f"🎧 Podcast de {city}"
        )
    send_log(datetime.now(), f"Sent podcast to user {user_id}.")

# resumen <ciudad>
async def resumen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    send_log(datetime.now(), f"User {user_id} requested a summary.")
    if not context.args:
        send_log(datetime.now(), f"User {user_id} did not provide a city for the summary.")
        await update.message.reply_text("Usa: /resumen <ciudad>")
        return

    city = " ".join(context.args)

    await update.message.chat.send_action(action="typing")
    await update.message.reply_text("🧠 Seleccionando noticias para ti...")
    news = get_news(city)

    profile = get_user_profile(user_id)
    user_preferences = profile["interests"] if profile and "interests" in profile else []
    send_log(datetime.now(), f"User {user_id} has interests: {user_preferences}.")

    curated_news = select_and_adapt_news(
        city=city,
        news=news,
        user_interests=user_preferences
    )
    await update.message.chat.send_action(action="typing")
    await update.message.reply_text("📄 Generando resumen...")

    summary = podcast_script(city, curated_news)
    send_log(datetime.now(), f"Generated daily summary for user {user_id}.")

    await update.message.reply_text(summary)
    send_log(datetime.now(), f"Sent daily summary to user {user_id}.")


# configure
user_temp_selection = {}

async def configure(update, context):
    user_id = update.effective_user.id
    user_temp_selection[user_id] = []
    send_log(datetime.now(), f"User {user_id} started configuration.")

    await update.message.reply_text(
        "Configura tus intereses: ",
        reply_markup = interests_keyboard()
    )

async def interests_callback(update, context):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    if user_id not in user_temp_selection:
        user_temp_selection[user_id] = []
    
    data = query.data
    send_log(datetime.now(), f"User {user_id} sent callback data: {data}.")

    if data.startswith("interest:"):
        interest = data.split(":")[1]
        selected = user_temp_selection[user_id]

        if interest in selected:
            selected.remove(interest)
        else:
            selected.append(interest)
        
        send_log(datetime.now(), f"User {user_id} temporary interests: {selected}.")

        await query.edit_message_reply_markup(
            reply_markup = interests_keyboard(selected)
        )
    elif data == "save_interests":
        set_users_interests(user_id, user_temp_selection[user_id])
        send_log(datetime.now(), f"User {user_id} saved interests: {user_temp_selection[user_id]}.")

        await query.edit_message_text(
            f"✅ Intereses guardados:\n\n"
            + ", ".join(user_temp_selection[user_id])
        )

        del user_temp_selection[user_id]

def interests_keyboard(selected=None):
    selected = selected or []

    keyboard = [
        [
            InlineKeyboardButton(
                f"{'✅' if interest in selected else '⬜'} {interest.capitalize()}",
                callback_data=f"interest:{interest}"
            )
        ]
        for interest in AVAILABLE_INTERESTS
    ]

    keyboard.append([
        InlineKeyboardButton("💾 Guardar", callback_data="save_interests")
    ])

    return InlineKeyboardMarkup(keyboard)



app = ApplicationBuilder().token("8328525433:AAEoUO1Eqb9X0zD58SCTvuOH4eflT-8Cg_M").build()

app.add_handler(CommandHandler("help", help))
app.add_handler(CommandHandler("podcast", podcast))
app.add_handler(CommandHandler("resumen", resumen))
app.add_handler(CommandHandler("configure", configure))

app.add_handler(
    CallbackQueryHandler(interests_callback)
)

send_log(datetime.now(), "Bot started.")
app.run_polling()