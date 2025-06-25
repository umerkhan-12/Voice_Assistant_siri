# 🎙️ Siri Voice Assistant (Python + AI + News + GUI)

A modern voice assistant built using Python, featuring AI-powered chat, real-time news fetching, natural speech output, and a GUI-based control panel. Say “Hey Siri” to activate voice commands and enjoy a smart, voice-controlled desktop experience.

---

## 🚀 Features

### 🧠 AI Chat Assistant
- Ask anything and get smart replies using **Cohere AI**.
- Example: “Chat with AI”, “What is quantum computing?”

### 📰 News Reader
- Say: “news” or “news about sports”
- Fetches real-time headlines using **NewsAPI**

### 🎧 Voice Input + Output
- Activates with the phrase **“Hey Siri”**
- Speaks responses using **Edge TTS** with natural-sounding voice

### 🌐 Smart Web Control
- Commands like “open YouTube”, “play Shape of You”
- Opens sites or performs YouTube searches using your default browser

### 🖥️ GUI Interface (Tkinter)
- 🎙️ Start Listening button
- 📜 Scrollable conversation history
- 🟢 Status indicator (Idle / Listening)

---

## 🧠 Core Logic & Advanced Concepts

This project combines multiple advanced programming and AI concepts:

### 1. 🗣️ **Voice Recognition**
- **Library:** `speech_recognition`
- Converts spoken audio to text using Google’s Web Speech API
- Handles noise using `adjust_for_ambient_noise()`
- Detects activation word: **“hey siri”**

### 2. 🗨️ **Natural Voice Output**
- **Libraries:** `edge-tts` (Microsoft neural TTS), `playsound`
- Uses `asyncio` to generate audio asynchronously
- Produces fast, human-like responses using `en-US-JennyNeural`

### 3. 🧠 **AI-Powered Chatbot**
- **Library:** `cohere`
- Sends user voice as prompt to Cohere’s **large language model**
- Receives intelligent text response and reads it out
- Enables dynamic AI conversation flow

### 4. 🌍 **Live News Fetching**
- **API:** NewsAPI.org
- **Library:** `requests`
- Fetches real-time news headlines or by topic
- Example: `https://newsapi.org/v2/everything?q=cricket`

### 5. 💻 **GUI & Multithreading**
- **Library:** `tkinter`
- Threading used to keep speech recognition non-blocking (`threading.Thread`)
- Dynamic GUI updates for status and output history
- Event-driven programming for button clicks and actions

### 6. 🌐 **Browser Automation**
- **Library:** `webbrowser`
- Dynamically opens websites based on voice command
- Example: “Search GitHub” opens `https://github.com`

---

## 📦 Tech Stack Summary

| Area             | Tool/Library         | Purpose                               |
|------------------|----------------------|----------------------------------------|
| Voice Input      | `speech_recognition` | Capture and convert spoken commands    |
| Voice Output     | `edge-tts`, `playsound` | Speak responses out loud           |
| AI Responses     | `cohere`             | Generate intelligent replies via LLM   |
| News Fetching    | `requests`, NewsAPI  | Get real-time news based on query      |
| GUI              | `tkinter`            | Interactive desktop interface          |
| Multithreading   | `threading`          | Handle speech recognition without freeze|
| Web Interaction  | `webbrowser`         | Open sites or perform searches         |
| Async Handling   | `asyncio`            | Asynchronous voice generation flow     |

---

## 🛠️ Installation

### 1. Clone or Download
```bash
git clone https://github.com/your-username/siri-voice-assistant
cd siri-voice-assistant


### install Depencies ###

pip install edge-tts cohere SpeechRecognition pyttsx3 requests playsound


Built by Umer — feel free to customize, fork, or improve!