import os

def send_log(date, message):
    os.makedirs("data", exist_ok=True)
    with open("data/logs.txt", "a", encoding="utf-8") as f:
        f.write(f"[{date}] {message}\n")

def get_log():
    with open("data/logs.txt", "r", encoding="utf-8") as f:
        return f.read()
