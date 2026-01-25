# 🎙️ Zarteando (NewsPodBot)

**Your Personal AI News Anchor on Telegram.**

> *Turn boring headlines into an engaging radio show.*

---

## 🧐 Why Zarteando?

We live in an age of information overload. Scrolling through dozens of news sites or reading dry headlines about your local city can be exhausting and time-consuming.

**Zarteando** was built to solve this. It transforms the latest news from any city into a **short, entertaining audio podcast**. Instead of reading, you listen to *Zarteando* (your AI host) narrate the day's events with a natural, radio-like personality. It's perfect for your commute, your morning coffee, or a quick catch-up while multitasking.

## ✨ Key Features

- **🌍 Hyper-Local Focus**: Instantly find and process relevant news for *any* specific city.
- **🧠 Intelligent Scriptwriting**: Powered by **Generative AI** (Ollama + Gemma 3), the bot doesn't just read text; it writes a fun, first-person radio script summarizing the events.
- **🗣️ Ultra-Realistic Narration**: Utilizes the **Murf API** to generate high-fidelity voice audio that sounds like a real human presenter.
- **📱 Seamless Telegram Integration**: Everything happens inside your chat. No external apps required.

---

## 🛠️ Tech Stack & Dependencies

This project leverages a modern stack of Python and AI technologies to deliver its functionality.

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Core Logic** | `Python 3.8+` | The backbone of the application. |
| **Bot Interface** | `python-telegram-bot` | Handles asynchronous communication with the Telegram API. |
| **News Source** | `GNews API` | Fetches real-time articles and metadata. |
| **Script Gen** | `Ollama` (Gemma 3:4b) | A local LLM server used to generate the creative script, ensuring privacy and cost-efficiency for text generation. |
| **Audio Engine** | `Murf API` | State-of-the-art Text-to-Speech (TTS) engine for lifelike audio. |
| **Audio Proc** | `pydub` | Used for audio file manipulation if necessary. |

---

## 🚀 Installation

### Prerequisites

1.  **Python 3.8** or higher.
2.  **Ollama** installed and running locally.
3.  **API Keys** for:
    *   Telegram Bot (@BotFather)
    *   GNews
    *   MURFApi

### Step-by-Step Guide

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/your-username/NewsPodBot.git
    cd NewsPodBot
    ```

2.  **Install Python Dependencies**
    ```bash
    pip install python-telegram-bot requests ollama murf pydub
    ```
    *(Note: `ffmpeg` may be required for pydub)*

3.  **Setup the AI Model**
    Pull the Gemma 3 model using Ollama:
    ```bash
    ollama pull gemma3:4b
    ```

4.  **Configuration**
    Currently, keys are set in the source files (Environment variables recommended for production).
    *   **Telegram Token**: Edit `src/bot.py`
    *   **GNews Key**: Edit `src/news.py`
    *   **TTS Config**: Edit `src/tts.py`

---

## ▶️ Usage

1.  **Start the Bot**
    ```bash
    python src/bot.py
    ```

2.  **Interact on Telegram**
    *   `/start` - Initialize and see options.
    *   `/podcast <City Name>` - Generate a news podcast for a specific city.
        *   *Example:* `/podcast Madrid`
    *   `/summary` - Get a quick text summary of top news.
    *   `/configure` - Set preferences like language.

---

*Created with ❤️ and Python.*
