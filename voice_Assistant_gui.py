import tkinter as tk
from tkinter import scrolledtext
import threading
import speech_recognition as sr
import pyttsx3
import webbrowser
import requests
import cohere
import os
import edge_tts
import asyncio
import playsound
from dotenv import load_dotenv




# API keys
load_dotenv() 

cohere_key = os.getenv("COHERE_API_KEY")
news_api = os.getenv("NEWS_API_KEY")
co = cohere.Client(cohere_key)

# Init
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# GUI Setup
root = tk.Tk()
root.title("Siri Voice Assistant")
root.geometry("800x700")

output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=30, width=80)
output_text.pack(pady=10)

status_label = tk.Label(root, text="Status: Idle", fg="green")
status_label.pack()

def update_output(text):
    output_text.insert(tk.END, text + "\n")
    output_text.see(tk.END)

def old_speak(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    async def edge_speak():
        communicate = edge_tts.Communicate(text, voice="en-US-JennyNeural", rate="+10%")
        await communicate.save("temp.mp3")
        playsound.playsound("temp.mp3")
        os.remove("temp.mp3")
    update_output("Assistant: " + text)
    asyncio.run(edge_speak())

def fetch_news(query=""):
    if query:
        url = f"https://newsapi.org/v2/everything?q={query}&pageSize=3&apiKey={news_api}"
    else:
        url = f"https://newsapi.org/v2/top-headlines?country=in&pageSize=3&apiKey={news_api}"
    try:
        response = requests.get(url)
        articles = response.json().get("articles", [])
        if not articles:
            speak("No news found.")
        for index, article in enumerate(articles, start=1):
                title = article.get("title", "")
                description = article.get("description", "")
                content = article.get("content", "")

                print(f"\n📰 {index}. {title}")
                print(f"Summary: {description}")
                print(f"Content: {content}")

                speak(f"News {index}: {title}")
                if description:
                    speak(description)
                elif content:
                    speak(content)  
                else:
                    speak("No details available.")
    except Exception as e:
        update_output(f"News Error: {e}")
        speak("Failed to fetch news.")

def ask_cohere(prompt):
    try:
        response = co.chat(message=prompt)
        reply = response.text
        update_output("Cohere: " + reply)
        speak(reply)
    except Exception as e:
        update_output("Cohere Error: " + str(e))
        speak("Could not respond from AI.")

def action_command(command):
        update_output("You: " + command)
        if "search" in command.lower():
            for name, url in {
                "youtube": "https://www.youtube.com",
                "facebook": "https://www.facebook.com",
                "google": "https://www.google.com",
                "instagram": "https://www.instagram.com",
                "github": "https://www.github.com",
                "stackoverflow": "https://stackoverflow.com",
                "whatsapp": "https://web.whatsapp.com",
                "twitter": "https://www.twitter.com",
                "gmail": "https://mail.google.com",
                "linkedin": "https://www.linkedin.com"
            }.items():
                if name in command.lower():
                    speak(f"Opening {name}")
                    webbrowser.open(url)
                    return
        elif "play" in command:
            song = command.replace("play", "")
            speak(f"Searching {song} on YouTube")
            webbrowser.open(f"https://www.youtube.com/results?search_query={song}")
        elif "news" in command:
            topic = command.replace("news", "").strip()
            if topic:
                speak(f"Getting news  {topic}")
                fetch_news(topic)
            else:
                speak("Getting top headlines")
                fetch_news()
        elif "chat" in command.lower() or "ai" in command.lower():
            speak("What would you like to ask?")
            with sr.Microphone() as source:
                audio = recognizer.listen(source, timeout=5)
                user_prompt = recognizer.recognize_google(audio)
                ask_cohere(user_prompt)
        elif "type with ai" in command.lower():
            user_input = input("Type your message: ")
            ask_cohere(user_input)
        elif "goodbye" in command or "exit" in command:
            speak("Goodbye!")
            bool_val=False
            root.quit()
        else:
            speak("Sorry, I didn't catch that.")

def chat_assistant():
    user_input = input("Type your message: ")
    if "quit" in user_input.lower():
        speak("Exiting chat assistant.")
        return
    ask_cohere(user_input)

def listen():
    try:
        status_label.config(text="Status: Listening...", fg="blue")
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            speak("Listening. Say Hey Siri.")
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio)
            print(f"Heard: {command}")
            if "hey siri" in command.lower():
                speak("Yes, how can I help?")
                audio = recognizer.listen(source, timeout=8,phrase_time_limit=8)
                command = recognizer.recognize_google(audio)
                if "chat" in command.lower() or "assistant" in command.lower():
                    print ("Chat assistant")
                    chat_assistant()
                else:
                    print(command)
                    action_command(command)
            else:
                speak("Say 'Hey Siri' to activate.")
    except Exception as e:
        update_output(f"Error: {e}")
        speak("Sorry, I couldn't understand.")
    finally:
        status_label.config(text="Status: Idle", fg="green")

def start_listening():
    threading.Thread(target=listen).start()

# Button
listen_btn = tk.Button(root, text="Start Listening 🎙️", command=start_listening, bg="blue", fg="white", font=("Arial", 12, "bold"))
listen_btn.pack(pady=20)

root.mainloop()
