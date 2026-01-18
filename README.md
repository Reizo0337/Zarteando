# Zarteando 🎙️📰

¡Bienvenido a **Zarteando**! Tu asistente personal de noticias en Telegram.

Este bot transforma las noticias de actualidad de cualquier ciudad en un **podcast de audio** corto, entretenido y narrado de forma natural. Olvídate de leer titulares aburridos; deja que *Zarteando* (tu presentador IA) te cuente lo que está pasando.

## ✨ Funcionalidades

- **🌍 Búsqueda Local:** Encuentra las noticias más relevantes de tu ciudad al instante.
- **🤖 Guionización Inteligente:** Utiliza IA Generativa (Ollama + Gemma 3) para crear un guion de radio divertido, cercano y en primera persona.
- **🗣️ Narración Ultra-Realista:** Convierte el guion en audio de alta calidad utilizando la API de ElevenLabs.
- **📱 Todo en Telegram:** Recibe el archivo de audio directamente en tu chat.

## 🛠️ Tecnologías Utilizadas

- **Python**: Lenguaje principal.
- **python-telegram-bot**: Para la interacción con la API de Telegram.
- **GNews API**: Fuente de noticias en tiempo real.
- **Ollama (Gemma 3:4b)**: Modelo de lenguaje local para la generación del guion.
- **ElevenLabs API**: Motor de Text-to-Speech (TTS).

## 🚀 Instalación y Requisitos

### Prerrequisitos
1. Tener **Python 3.8+** instalado.
2. Tener **Ollama** instalado y ejecutándose localmente.
3. Claves de API para: Telegram Bot, GNews y ElevenLabs.

### Pasos

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/tu-usuario/NewsPodBot.git
   cd NewsPodBot
   ```

2. **Instala las dependencias:**
   ```bash
   pip install python-telegram-bot requests ollama
   ```

3. **Descarga el modelo de IA:**
   Asegúrate de tener el modelo `gemma3:4b` en Ollama:
   ```bash
   ollama pull gemma3:4b
   ```

## ⚙️ Configuración

Actualmente, las credenciales se configuran directamente en los archivos fuente (se recomienda usar variables de entorno en producción). Revisa y actualiza los siguientes archivos con tus claves:

- **Telegram Token:** En `src/bot.py`
- **GNews API Key:** En `src/news.py`
- **ElevenLabs Config:** En `src/tts.py`

## ▶️ Uso

1. **Inicia el bot:**
   ```bash
   python src/bot.py
   ```

2. **En Telegram:**
   - Envía `/start` para ver las opciones.
   - Envía `/podcast <ciudad>` para generar tu noticiero.
     - *Ejemplo:* `/podcast Madrid`

---
*Creado con ❤️ y Python.*
