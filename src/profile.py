from config import AVAILABLE_INTERESTS
import json
from pathlib import Path
import os
from datetime import datetime
from utils import send_log

DATA_DIR = "data"
DATA_FILE = Path(DATA_DIR) / "user_preferences.json"

def ensure_storage():
    """Ensures that the data directory and file exist."""
    try:
        if not os.path.exists(DATA_DIR):
            send_log(datetime.now(), f"Data directory not found. Creating '{DATA_DIR}'.")
            os.makedirs(DATA_DIR)
        
        if not os.path.exists(DATA_FILE):
            send_log(datetime.now(), f"Data file not found. Creating '{DATA_FILE}'.")
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump({}, f)
    except OSError as e:
        send_log(datetime.now(), f"Error ensuring storage directory and file: {e}")


def load_users():
    """Loads all user profiles from the JSON file."""
    ensure_storage()
    try:
        if DATA_FILE.exists():
            send_log(datetime.now(), "Loading user profiles.")
            return json.loads(DATA_FILE.read_text(encoding="utf-8"))
        else:
            send_log(datetime.now(), "User profiles file does not exist, returning empty data.")
            return {}
    except (json.JSONDecodeError, FileNotFoundError) as e:
        send_log(datetime.now(), f"Error loading user profiles: {e}")
        return {}

def save_users(data):
    """Saves all user profiles to the JSON file."""
    ensure_storage()
    try:
        send_log(datetime.now(), "Saving user profiles.")
        DATA_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        send_log(datetime.now(), "User profiles saved successfully.")
    except IOError as e:
        send_log(datetime.now(), f"Error saving user profiles: {e}")


def set_users_interests(user_id, interests):
    """Sets the interests for a specific user."""
    send_log(datetime.now(), f"Setting interests for user {user_id}: {interests}")
    users = load_users()
    user_id = str(user_id)

    if user_id not in users:
        send_log(datetime.now(), f"New user {user_id}. Creating profile.")
        users[user_id] = {}

    users[user_id]["interests"] = interests
    save_users(users)
    send_log(datetime.now(), f"Interests for user {user_id} updated.")

def set_users_lang(user_id, lang):
    send_log(datetime.now, f"Setting language for user {user_id}: {lang}")
    users = load_users()
    user_id = str(user_id)

    if user_id not in users:
        send_log(datetime.now(), f"New user {user_id}. Creating profile.")
        users[user_id] = {}

    users[user_id]["lang"] = lang
    save_users(users)
    send_log(datetime.now(), f"Language for user {user_id} updated.")


def get_user_profile(user_id):
    """Retrieves the profile for a specific user."""
    send_log(datetime.now(), f"Getting profile for user {user_id}.")
    users = load_users()
    profile = users.get(str(user_id))
    if profile:
        send_log(datetime.now(), f"Profile found for user {user_id}.")
    else:
        send_log(datetime.now(), f"No profile found for user {user_id}.")
    return profile