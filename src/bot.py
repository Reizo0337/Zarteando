from datetime import datetime
import os
import asyncio
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
from telegram.error import BadRequest

from news import get_news
from content import podcast_script, select_and_adapt_news, daily_summary, daily_news_script
from scheduler import scheduler_manager, handle_dailynews_logic
from tts import generate_tts as text_to_audio
from profile import set_users_interests, get_user_profile, set_users_lang, get_user_lang
from config import AVAILABLE_INTERESTS, AVAILABLE_LANGS
from utils import send_log
from translations import get_translation
from diagnostics import print_diagnostics

# Store temporary selections
user_temp_selection = {}

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_lang = get_user_lang(user_id)
    
    # Initialize onboarding flow
    user_temp_selection[user_id] = {'lang': user_lang, 'onboarding': True}
    
    await update.message.reply_text(
        get_translation(user_lang, "welcome_message"),
        reply_markup=language_keyboard(user_lang, user_lang)
    )

# /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_lang = get_user_lang(user_id)
    send_log(datetime.now(), f"User {user_id} requested help in {user_lang}.")
    await update.message.reply_text(get_translation(user_lang, "help_message"))

# /podcast <city>
async def podcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_lang = get_user_lang(user_id)
    send_log(datetime.now(), f"User {user_id} requested a podcast in {user_lang}.")

    if not context.args:
        send_log(datetime.now(), f"User {user_id} did not provide a city for the podcast.")
        await update.message.reply_text(get_translation(user_lang, "podcast_usage"))
        return

    city = " ".join(context.args)
    send_log(datetime.now(), f"User {user_id} requested a podcast for city: {city}.")

    await update.message.chat.send_action(action="typing")
    await update.message.reply_text(get_translation(user_lang, "searching_news"))

    news = await get_news(city, lang=user_lang)
    if not news:
        send_log(datetime.now(), f"No news found for city: {city}.")
        await update.message.reply_text(get_translation(user_lang, "no_news_found"))
        return
    
    send_log(datetime.now(), f"Found {len(news)} news articles for city: {city}.")

    profile = get_user_profile(user_id)
    user_preferences = profile.get("interests", []) if profile else []
    send_log(datetime.now(), f"User {user_id} has interests: {user_preferences}.")

    await update.message.chat.send_action(action="typing")
    await update.message.reply_text(get_translation(user_lang, "selecting_news"))

    curated_news = await select_and_adapt_news(
        city=city,
        news=news,
        user_interests=user_preferences,
        lang=user_lang
    )
    send_log(datetime.now(), f"Curated news for user {user_id}, {curated_news}.")

    await update.message.chat.send_action(action="typing")
    await update.message.reply_text(get_translation(user_lang, "generating_script"))
    
    script = await podcast_script(city, curated_news, lang=user_lang)
    send_log(datetime.now(), f"Generated podcast script for user {user_id}.")

    await update.message.chat.send_action(action="record_audio")

    audio_path = await text_to_audio(script, lang=user_lang)
    if not audio_path:
        send_log(datetime.now(), f"Error generating audio for user {user_id}.")
        await update.message.reply_text(get_translation(user_lang, "error_generating_audio"))
        return
        
    send_log(datetime.now(), f"Generated audio at {audio_path} for user {user_id}.")

    with open(audio_path, "rb") as audio:
        await update.message.reply_voice(
            voice=audio,
            caption=get_translation(user_lang, "podcast_caption", city=city),
            read_timeout=120,
            write_timeout=120
        )
    send_log(datetime.now(), f"Sent podcast to user {user_id}.")

# /resumen <city>
async def resumen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_lang = get_user_lang(user_id)
    send_log(datetime.now(), f"User {user_id} requested a summary in {user_lang}.")

    if not context.args:
        await update.message.reply_text(get_translation(user_lang, "summary_usage"))
        return

    city = " ".join(context.args)

    await update.message.chat.send_action(action="typing")
    await update.message.reply_text(get_translation(user_lang, "selecting_news"))
    news = await get_news(city, lang=user_lang)

    profile = get_user_profile(user_id)
    user_preferences = profile.get("interests", []) if profile else []
    
    curated_news = await select_and_adapt_news(
        city=city,
        news=news,
        user_interests=user_preferences,
        lang=user_lang
    )
    await update.message.chat.send_action(action="typing")
    await update.message.reply_text(get_translation(user_lang, "generating_summary"))

    summary = await daily_summary(city, curated_news, lang=user_lang)
    await update.message.reply_text(summary)
    send_log(datetime.now(), f"Sent daily summary to user {user_id}.")

# /dailynews <city> <time>
bot_loop = None

async def execute_daily_news(chat_id, city):
    user_lang = get_user_lang(chat_id)
    send_log(datetime.now(), f"Executing daily news for {chat_id} in {city} ({user_lang}).")
    
    news = await get_news(city, lang=user_lang)
    if not news:
        send_log(datetime.now(), f"No news found for daily podcast in {city}.")
        return

    profile = get_user_profile(chat_id)
    user_preferences = profile.get("interests", []) if profile else []
    
    curated_news = await select_and_adapt_news(
        city=city,
        news=news,
        user_interests=user_preferences,
        lang=user_lang
    )
    
    script = await daily_news_script(city, curated_news, lang=user_lang)
    audio_path = await text_to_audio(script, lang=user_lang)
    
    if audio_path:
        with open(audio_path, "rb") as audio:
            await app.bot.send_voice(
                chat_id=chat_id,
                voice=audio,
                caption=get_translation(user_lang, "podcast_caption", city=city),
                read_timeout=120,
                write_timeout=120
            )
        send_log(datetime.now(), f"Sent daily podcast to {chat_id}.")
    else:
        send_log(datetime.now(), f"Failed to generate audio for daily podcast {chat_id}.")

def trigger_daily_news(chat_id, city):
    if bot_loop:
        asyncio.run_coroutine_threadsafe(execute_daily_news(chat_id, city), bot_loop)

async def dailynews(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_lang = get_user_lang(user_id)
    
    if not context.args:
        await update.message.reply_text(get_translation(user_lang, "dailynews_usage"))
        return

    success, city, time_str = handle_dailynews_logic(user_id, context.args, trigger_daily_news)
    
    if success:
        await update.message.reply_text(
            get_translation(user_lang, "dailynews_scheduled", city=city, time=time_str)
        )
    else:
        await update.message.reply_text(get_translation(user_lang, "dailynews_usage"))

async def stopdailynews(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_lang = get_user_lang(user_id)
    
    if not context.args:
        await update.message.reply_text(get_translation(user_lang, "stopdailynews_usage"))
        return

    city = " ".join(context.args)
    success = scheduler_manager.remove_daily_job(user_id, city)
    
    if success:
        await update.message.reply_text(get_translation(user_lang, "stopdailynews_success", city=city))
    else:
        await update.message.reply_text(get_translation(user_lang, "stopdailynews_not_found", city=city))

# /language
async def language_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_lang = get_user_lang(user_id)
    user_temp_selection[user_id] = {'lang': user_lang}
    
    await update.message.reply_text(
        get_translation(user_lang, "language_config"),
        reply_markup=language_keyboard(user_lang, user_lang)
    )

def language_keyboard(user_lang, selected_lang):
    keyboard = [
        [
            InlineKeyboardButton(
                f"{'🔵' if lang == selected_lang else '⚪️'} {lang.upper()}",
                callback_data=f"language:{lang}"
            )
        ]
        for lang in AVAILABLE_LANGS
    ]
    keyboard.append([
        InlineKeyboardButton(get_translation(user_lang, "save"), callback_data="save_lang")
    ])
    return InlineKeyboardMarkup(keyboard)

# /configure
async def configure(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_lang = get_user_lang(user_id)
    profile = get_user_profile(user_id)
    user_interests = profile.get("interests", []) if profile else []
    user_temp_selection[user_id] = {'interests': user_interests.copy()}
    
    await update.message.reply_text(
        get_translation(user_lang, "interests_config"),
        reply_markup=interests_keyboard(user_lang, user_interests)
    )

def interests_keyboard(user_lang, selected_interests):
    interest_translations = get_translation(user_lang, "interests")
    keyboard = [
        [
            InlineKeyboardButton(
                f"{'✅' if interest in selected_interests else '⬜️'} {interest_translations.get(interest, interest.capitalize())}",
                callback_data=f"interest:{interest}",
            )
        ]
        for interest in AVAILABLE_INTERESTS
    ]
    keyboard.append([
        InlineKeyboardButton(get_translation(user_lang, "save"), callback_data="save_interests")
    ])
    return InlineKeyboardMarkup(keyboard)

# Unified Callback Handler
async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    user_lang = get_user_lang(user_id)
    await query.answer()

    if user_id not in user_temp_selection:
        # Initialize with current settings if not in temp selection
        profile = get_user_profile(user_id)
        user_interests = profile.get("interests", []) if profile else []
        user_temp_selection[user_id] = {'interests': user_interests, 'lang': user_lang}

    data = query.data
    send_log(datetime.now(), f"User {user_id} sent callback data: {data}")

    # Language selection
    if data.startswith("language:"):
        lang = data.split(":")[1]
        user_temp_selection[user_id]['lang'] = lang
        # Get the language of the user who is interacting for the keyboard language
        interaction_lang = user_temp_selection[user_id].get('lang', user_lang)
        try:
            await query.edit_message_reply_markup(
                reply_markup=language_keyboard(interaction_lang, lang)
            )
        except BadRequest as e:
            if "Message is not modified" not in str(e):
                raise

    elif data == "save_lang":
        selected_lang = user_temp_selection[user_id].get('lang', user_lang)
        set_users_lang(user_id, selected_lang)
        send_log(datetime.now(), f"User {user_id} saved language: {selected_lang}.")
        
        # Check if this is part of onboarding
        if user_temp_selection[user_id].get('onboarding'):
            # Proceed to interests configuration
            profile = get_user_profile(user_id)
            user_interests = profile.get("interests", []) if profile else []
            user_temp_selection[user_id]['interests'] = user_interests
            
            await query.edit_message_text(
                get_translation(selected_lang, "lets_configure_interests"),
                reply_markup=interests_keyboard(selected_lang, user_interests)
            )
        else:
            await query.edit_message_text(
                get_translation(selected_lang, "language_saved", language_name=selected_lang.upper())
            )
            if user_id in user_temp_selection:
                del user_temp_selection[user_id]

    # Interest selection
    elif data.startswith("interest:"):
        interest = data.split(":")[1]
        selected = user_temp_selection[user_id].get('interests', [])
        if interest in selected:
            selected.remove(interest)
        else:
            selected.append(interest)
        user_temp_selection[user_id]['interests'] = selected
        try:
            await query.edit_message_reply_markup(
                reply_markup=interests_keyboard(user_lang, selected)
            )
        except BadRequest as e:
            if "Message is not modified" not in str(e):
                raise

    elif data == "save_interests":
        selected_interests = user_temp_selection[user_id].get('interests', [])
        set_users_interests(user_id, selected_interests)
        send_log(datetime.now(), f"User {user_id} saved interests: {selected_interests}.")
        
        # Refresh lang in case it changed during onboarding
        current_lang = get_user_lang(user_id)
        
        if user_temp_selection[user_id].get('onboarding'):
            await query.edit_message_text(get_translation(current_lang, "setup_complete"))
        else:
            interest_translations = get_translation(current_lang, "interests")
            translated_interests = [interest_translations.get(i, i.capitalize()) for i in selected_interests]
            await query.edit_message_text(
                get_translation(current_lang, "interests_saved") + ", ".join(translated_interests)
            )
        if user_id in user_temp_selection:
            del user_temp_selection[user_id]

async def post_init(application):
    global bot_loop
    bot_loop = asyncio.get_running_loop()
    scheduler_manager.load_jobs(trigger_daily_news)
    scheduler_manager.start()

import os
from dotenv import load_dotenv

load_dotenv()

app = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).post_init(post_init).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("podcast", podcast))
app.add_handler(CommandHandler("resumen", resumen))
app.add_handler(CommandHandler("dailynews", dailynews))
app.add_handler(CommandHandler("stopdailynews", stopdailynews))
app.add_handler(CommandHandler("language", language_command))
app.add_handler(CommandHandler("configure", configure))
app.add_handler(CallbackQueryHandler(callback_handler))

print_diagnostics()
send_log(datetime.now(), "Bot started.")
app.run_polling()
