from ollama import Client
from datetime import datetime
from utils import send_log
from translations import get_translation
from deep_translator import GoogleTranslator

client = Client()

def translate_prompt(prompt, lang):
    if lang == "en":
        return prompt  # No need to translate if it's already in English
    try:
        return GoogleTranslator(source='auto', target=lang).translate(prompt)
    except Exception as e:
        send_log(datetime.now(), f"Error translating prompt to {lang}: {e}")
        return prompt # Return original prompt on error

def podcast_script(city, filtered_news_text, lang="es"):
    send_log(datetime.now(), f"Generating podcast script for city: {city} in {lang}.")

    base_prompt = f"""
        Generate a podcast script about today's news in {city}.
        The style should be close and natural, as if you were telling a friend about the news.
        Add subtle jokes between news, or even give opinions on the topics.
        It has to be entertaining, with a short introduction mentioning the news headlines.

        Script structure:
        1. Introduction
        2. News
        3. Conclusion

        News:
        {filtered_news_text}

        Your name is Zarteando. You are the host. Don't mention music or sound effects. Just the dialogue.
        The podcast is 1-on-1, you talking to the user.

        NO MORE THAN 2-3 MINUTES PER PODCAST.
        """
    
    prompt = translate_prompt(base_prompt, lang)

    try:
        response = client.generate(
            model="gemma3:4b",
            prompt=prompt,
        )
        script = response.get("response", "")
        send_log(datetime.now(), f"Successfully generated podcast script for city: {city} in {lang}.")
        return script
    except Exception as e:
        send_log(datetime.now(), f"Error generating podcast script for city {city} in {lang}: {e}")
        return get_translation(lang, "error_generating_script", city=city)


def daily_summary(city, news, lang="es"):
    send_log(datetime.now(), f"Generating daily summary for city: {city} in {lang}.")
    
    base_prompt = f"Summarize today's most important news in {city}:\n{news}"
    prompt = translate_prompt(base_prompt, lang)

    try:
        response = client.generate(
            model="gemma3:4b",
            prompt=prompt,
        )
        summary = response.get("response", "")
        send_log(datetime.now(), f"Successfully generated daily summary for city: {city} in {lang}.")
        return summary
    except Exception as e:
        send_log(datetime.now(), f"Error generating daily summary for city {city} in {lang}: {e}")
        return get_translation(lang, "error_generating_summary", city=city)

def select_and_adapt_news(city, news, user_interests, lang="es"):
    send_log(datetime.now(), f"Selecting and adapting news for city: {city} with interests: {user_interests} in {lang}.")
    
    news_block = "\n\n".join(
        f"NEWS {i+1}: Title: {n['title']}\nDescription: {n['description']}"
        for i, n in enumerate(news)
    )

    interests_text = ", ".join(user_interests)

    base_prompt = f"""
        Your role is a news editor and podcast host.
        User profile:
        - City: {city}
        - Main interests: {interests_text}

        Task:
        1. Read all the news provided below.
        2. Filter the news based on the user's interests. If no news matches, select the most relevant ones.
        3. Adapt the tone and content to the user's preferences. You can add humor related to their interests. DO NOT CHANGE OR INVENT FACTS ABOUT THE NEWS.
        4. Prioritize quality and relevance, not quantity.

        Return the result as an ordered list of selected news,
        keeping the title and a brief explanation of why it is relevant.

        Available news:
        {news_block}
        """
    
    prompt = translate_prompt(base_prompt, lang)

    try:
        response = client.generate(
            model="gemma3:4b",
            prompt=prompt
        )
        curated_news = response.get("response", "")
        send_log(datetime.now(), f"Successfully selected and adapted news for city: {city} in {lang}.")
        return curated_news
    except Exception as e:
        send_log(datetime.now(), f"Error selecting and adapting news for city {city} in {lang}: {e}")
        return get_translation(lang, "error_selecting_news", city=city)