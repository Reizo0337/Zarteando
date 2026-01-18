from config import AVAILABLE_INTERESTS
import json
from pathlib import Path
import os

DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "user_preferences.json")
DATA_FILE = Path(DATA_DIR + "/user_preferences.json")

def ensure_storage():
    # creamos carpeta y archivo si no existe
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)

def load_users():
    ensure_storage()

    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    
    return {}

def save_users(data):
    ensure_storage()
    DATA_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

def set_users_interests(user_id, interests):
    users = load_users()
    user_id = str(user_id)

    if user_id not in users:
        users[user_id] = {}

    users[user_id]["interests"] = interests
    save_users(users)

def get_user_profile(user_id):
    users = load_users()
    return users.get(str(user_id))