import speech_recognition as sr
import webbrowser
import pyttsx3
import tkinter as tk
import requests
import cohere
from dotenv import load_dotenv
import playsound
import os
import edge_tts
import asyncio
# import openai
# from openai import OpenAI
load_dotenv() 

cohere_key = os.getenv("COHERE_API_KEY")
news_api = os.getenv("NEWS_API_KEY")

co = cohere.Client(cohere_key)



recognizer = sr.Recognizer()
engine =pyttsx3.init()

def old_speak(text):
    # output_text.set(text)
    engine.say(text)
    engine.runAndWait()

def speak(text):
     async def edge_speak():
        communicate = edge_tts.Communicate(text, voice="en-US-JennyNeural", rate="+10%")
        await communicate.save("temp.mp3")
        playsound.playsound("temp.mp3")
        os.remove("temp.mp3")

     asyncio.run(edge_speak())



def fetch_news(query=""):
    if query:
        url = f"https://newsapi.org/v2/everything?q={query}&pageSize=5&apiKey={news_api}"
    else:
        url = f"https://newsapi.org/v2/top-headlines?country=in&pageSize=5&apiKey={news_api}"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            articles = data.get("articles", [])
            if not articles:
                speak("Sorry, no news found.")
                print("No articles found.")
                return

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

        else:
            speak("Sorry, I couldn't fetch the news right now.")
            print("News API error:", response.status_code)

    except Exception as e:
        print("News Error:", e)
        speak("There was an error fetching the news.")

def ask_cohere(prompt):
    try:
        response = co.chat(message=prompt)
        reply = response.text
        print("Cohere:", reply)
        speak(reply)
    except Exception as e:
        print("Cohere Error:", e)
        speak("Sorry, I couldn't get a response from Cohere.")

def action_command(command):
    # if search for browser
    if "search" in command.lower():
        site_urls = {
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
        }
        
        for name  in site_urls:
            if name in command.lower():
                speak(f"Search {name} browser")
                webbrowser.open(site_urls[name])
       # Treat the command as a song name
    elif "play" in command.lower():
        song = command.lower().replace("play","")
        print(song)
        speak(f"Searching YouTube for {song}")
        search_url = f"https://www.youtube.com/results?search_query={song}"
        webbrowser.open(search_url)
        #  want news by using news api fetching news
    elif "news" in command.lower():
    # Extract topic after the word "news"
        print(command)
        words = command.lower().replace("news","")
        print(words)
        if len(words) > 1:
            # topic = " ".join(words[1:])  # e.g. "about cricket"
            # print(topic)
            speak(f"Getting news about {words}")
            fetch_news(words)
        else:
            speak("Getting top headlines.")
            fetch_news()
    # ask cohere or ai 
    elif "chat" or "with ai" in command.lower():
        speak("What do you want to ask?")
        with sr.Microphone() as source:
            audio = recognizer.listen(source, timeout=5)
            user_prompt = recognizer.recognize_google(audio)
            ask_cohere(user_prompt)
    #    if want to exit
    elif "good bye" in command.lower():
         speak("Thank you! Bye bye")
         exit()
    else:
        speak("I dont get any voice please say clearly")
        
       
    


if __name__ == "__main__":

    speak("Initializing Siri.....")
    

    # make function for listening using speech recongnition functions 
    while True:
        recognizer = sr.Recognizer()
        print("Recongnizing...")

        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=1)
                print("listening...")
                audio = recognizer.listen(source)
            command =recognizer.recognize_google(audio)
            # print(command)
            
            if "hey siri" in command.lower():
                speak("yes")
                # activate siri
                with sr.Microphone() as source:
                    print("Activate siri...")
                    audio = recognizer.listen(source,timeout=5,phrase_time_limit=6)
                    command =recognizer.recognize_google(audio)
                    # print(command)
                    action_command(command)
            else:
                speak("Please say first say hey siri then i take your command")        
        except Exception as e:
            print(f"Error :{e} ".format(e))
            








