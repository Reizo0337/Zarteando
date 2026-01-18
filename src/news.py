import requests

API_KEY = "85d6761cdd6db8b5f3dab3a18c3ef144"

def get_news(city):
    url = "https://gnews.io/api/v4/search"
    params = {
        "q": city,
        "lang": "es",
        "token": API_KEY
    }
    r = requests.get(url, params=params)
    data = r.json()
    
    print("TOTAL RESULTS:", len(data.get("articles", [])))  # debug

    return [
        {
            "title": a["title"],
            "description": a.get("description", ""),
            "source": a["source"]["name"],
            "url": a["url"]
        }
        for a in data.get("articles", [])
    ]
