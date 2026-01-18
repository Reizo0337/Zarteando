# daf06de2ec514832811a98556b60b8f6
import requests
from datetime import date

API_KEY = "daf06de2ec514832811a98556b60b8f6"


def get_news(city, limit):
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "apiKey": API_KEY,
        "q": city,
        "language": "es",
        "sortBy" : "relevancy",
        "from": date.today().isoformat(),
    
        "pageSize": limit
    }

    r = requests.get(url, params=params)
    articles = r.json().get("articles", [])
    return [
        {
            "title": a["title"],
            "description": a["description"],
            "source": a["source"]["name"],
            "url": a["url"],
        }
        for a in articles
    ]