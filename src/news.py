import requests
import os
import asyncio

from dotenv import load_dotenv
from datetime import datetime
from utils import send_log


load_dotenv()
API_KEY = os.getenv("GNEWS_API_KEY")


def _get_news_sync(city, lang="es"):
    send_log(datetime.now(), f"Fetching news for city: {city}.")
    url = "https://gnews.io/api/v4/search"
    params = {
        "q": city,
        "lang": lang,
        "token": API_KEY
    }
    try:
        r = requests.get(url, params=params)
        r.raise_for_status()  # Raise an exception for bad status codes
        data = r.json()
        
        articles = data.get("articles", [])
        send_log(datetime.now(), f"Found {len(articles)} articles for city: {city}.")

        # The user had a print here, I'll keep it as a log.
        send_log(datetime.now(), f"TOTAL RESULTS for {city}: {len(articles)}")


        return [
            {
                "title": a["title"],
                "description": a.get("description", ""),
                "source": a["source"]["name"],
                "url": a["url"]
            }
            for a in articles
        ]
    except requests.exceptions.RequestException as e:
        send_log(datetime.now(), f"Error fetching news for city {city}: {e}")
        return []
    except Exception as e:
        send_log(datetime.now(), f"An unexpected error occurred while fetching news for {city}: {e}")
        return []

async def get_news(city, lang="es"):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, _get_news_sync, city, lang)
