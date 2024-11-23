import pvporcupine
import pvrecorder
import pyttsx3
import speech_recognition as sr
from datetime import datetime
import webbrowser
from pytube import Search
import requests  # For making API requests
import re  # For extracting city name from command
import wikipedia  # For fetching Wikipedia summaries
import yt_dlp
import sqlite3
import pygame
import random
import pywhatkit as kit
import time
import threading
import win32gui
import os
import schedule
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

# Initialize pyttsx3 engine only once
engine = pyttsx3.init()


# OpenWeatherMap API details
API_KEY = "df609a094fb3e0f3de0caf4c8265c2a5"  ######## WeatherMap API key #########
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

NEWS_API_KEY = "pub_57529749d229a820456ae31d1b3a5985783a4"
NEWSDATA_URL = "https://newsdata.io/api/1/latest?apikey=" + NEWS_API_KEY + "&country=in&prioritydomain=top"

    


def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for a command...")
        audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that.")
            return None
        except sr.RequestError:
            print("Request failed; check your network connection.")
            return None

def play_song(song_name):
    try:
        speak(f"Searching for {song_name} on YouTube")
        print(f"Searching for {song_name} on YouTube")
        
        # Search for the song on YouTube
        search = Search(song_name)
        video = search.results[0]  # Get the first result

        # Open the video in the web browser
        video_url = f"https://www.youtube.com/watch?v={video.video_id}"
        webbrowser.open(video_url)
        
        speak(f"Playing {song_name}")
        print(f"Playing {song_name}: {video_url}")
    except Exception as e:
        speak("I couldn't find the song. Please try again.")
        print(f"Error playing song: {e}")

def get_weather(city):
    try:
        # Build the complete API call URL
        url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        weather_data = response.json()
        
        if weather_data["cod"] != "404":
            main = weather_data['main']
            temperature = main['temp']
            humidity = main['humidity']
            weather_description = weather_data['weather'][0]['description']

            # Format the response
            weather_report = (f"The temperature in {city} is {temperature}°C with "
                              f"{weather_description}. Humidity is {humidity}%.")

            speak(weather_report)
            print(weather_report)
            print(f"Fetching weather for: {city}")
        else:
            speak("City not found. Please try again.")
            print("City not found.")
    except Exception as e:
        speak("Sorry, I couldn't fetch the weather details.")
        print(f"Error fetching weather: {e}")

# Wikipedia search function
def get_wikipedia_summary(subject):
    try:
        summary = wikipedia.summary(subject, sentences=3)  # Get a brief summary (2 sentences)
        print(summary)
        speak(summary)
    except wikipedia.exceptions.PageError:
        speak("Sorry, I couldn't find any information on that topic.")
        print(f"No Wikipedia page found for {subject}.")
    except wikipedia.exceptions.DisambiguationError as e:
        print(f"Disambiguation error for {subject}: {e.options}")
        speak(f"There are multiple results for {subject}. Please be more specific.")
    except Exception as e:
        speak("An error occurred while fetching Wikipedia information.")
        print(f"Error fetching Wikipedia summary: {e}")
        



def get_news_headlines():
    try:
        # Fetch news from the NewsData API only
        response = requests.get(NEWSDATA_URL)
        newsdata_response = response.json()
        print("Newsdata.io API Response:", newsdata_response)  # Debugging response

        if newsdata_response.get("status") == "success" and newsdata_response.get("results"):
            articles = newsdata_response["results"][:5]
            headlines = [article["title"] for article in articles]
            for idx, headline in enumerate(headlines, 1):
                print(f"Headline {idx}: {headline}")
                speak(f"Headline {idx}: {headline}")
        else:
            speak("Sorry, I couldn't fetch the news right now.")
            print("No articles found or failed to retrieve news.")
    except Exception as e:
        speak("An error occurred while fetching the news.")
        print(f"Error fetching news: {e}")




def setup_database():
    conn = sqlite3.connect('songs.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY,
            song_name TEXT NOT NULL,
            genre TEXT NOT NULL,
            path TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    

# Insert sample data into the database
def add_songs():
    conn = sqlite3.connect('songs.db')
    cursor = conn.cursor()
    songs = [
        ("Song1", "melody", "C:/Users/yadun/OneDrive/Desktop/123/melody/[iSongs.info] 02 - Neenaade Naa.mp3"),
        ("Song2", "rock", "C:/Users/yadun/OneDrive/Desktop/speech/[iSongs.info] 05 - Feel The Power.mp3"),
        # Add more songs for each genre...
    ]
    cursor.executemany('INSERT INTO songs (song_name, genre, path) VALUES (?, ?, ?)', songs)
    conn.commit()
    conn.close()

setup_database()
add_songs()



def play_songs_by_genre(genre):
    conn = sqlite3.connect('songs.db')
    cursor = conn.cursor()
    cursor.execute('SELECT song_name, path FROM songs WHERE genre = ?', (genre,))
    songs = cursor.fetchall()
    conn.close()

    for song in songs:
        song_name, song_url = song
        print(f"Playing {song_name}")
        speak(f"Playing {song_name}")
        webbrowser.open(song_url)
        time.sleep(60)  # 1-minute interval

# Schedule based on your time slots
def handle_radio_command():
    current_hour = datetime.now().hour

    if 6 <= current_hour < 7:
        genre = "devotional"
    elif 20 <= current_hour < 21:
        genre = "rock"
    elif 9 <= current_hour < 11:
        genre = "romantic"
    elif 11 <= current_hour < 13:
        genre = "melody"
    elif 13 <= current_hour < 15:
        genre = "pop"
    elif 15 <= current_hour < 18:
        genre = "evergreen"
    else:
        speak("Radio is off during these hours.")
        return

    play_songs_by_genre(genre)




def process_command(command):
    if 'radio' in command:
        # speak("Starting the radio.")
        handle_radio_command()
        return "Checking with Radio"
    elif any(word in command for word in ['news', 'headlines']):
        get_news_headlines()
    elif 'time' in command:
        current_time = datetime.now().strftime('%H:%M')
        speak(f"The current time is {current_time}")
    elif 'date' in command:
        current_date = datetime.now().strftime('%Y-%m-%d')
        speak(f"Today's date is {current_date}")
    elif 'play' in command:
        song_name = command.replace('play', '').strip()
        play_song(song_name)
    elif 'weather' in command:
        city_match = re.search(r'weather in ([a-zA-Z\s]+)', command)
        if city_match:
            city = city_match.group(1).strip()
            get_weather(city)
        else:
            speak("Please specify the city.")
    elif 'wikipedia' in command or 'tell me about' in command or 'information about' in command or 'what is' in command:
        subject = re.search(r'(wikipedia|tell me about|information about)\s+(.+)', command)
        if subject:
            search_query = subject.group(2).strip()
            get_wikipedia_summary(search_query)
        else:
            speak("Please specify a subject to search on Wikipedia.")
    elif 'exit' in command or 'stop' in command:
        speak("Goodbye!")
        exit()
    else:
        speak("I'm not sure how to respond to that.")



def wake_word_detection():
    porcupine = None
    recorder = None

    try:
        access_key = "w3jTQyFKjnjUMcr+VhkMnOJAb4MHMlY1QagWDc05ZEvMCTTfFngEVQ=="

        porcupine = pvporcupine.create(access_key=access_key, keywords=['jarvis'])

        recorder = pvrecorder.PvRecorder(device_index=-1, frame_length=porcupine.frame_length)
        recorder.start()

        print("Listening for the wake word...")

        while True:
            pcm = recorder.read()
            keyword_index = porcupine.process(pcm)

            if keyword_index >= 0:
                print("Wake word detected!")
                speak("hmm")
                return True

    finally:
        if porcupine:
            porcupine.delete()
        if recorder:
            recorder.stop()
            recorder.delete()


class VoiceAssistantUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice Assistant")

        # Log area
        self.log_area = ScrolledText(root, wrap=tk.WORD, state='disabled', height=15)
        self.log_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Command input
        self.input_frame = tk.Frame(root)
        self.input_frame.pack(padx=10, pady=5, fill=tk.X)
        self.command_entry = tk.Entry(self.input_frame, width=50)
        self.command_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.command_entry.bind('<Return>', self.send_command)

        self.send_button = tk.Button(self.input_frame, text="Send", command=self.send_command)
        self.send_button.pack(side=tk.RIGHT, padx=5)

        # Control buttons
        self.control_frame = tk.Frame(root)
        self.control_frame.pack(padx=10, pady=10)
        self.start_button = tk.Button(self.control_frame, text="Start Assistant", command=self.start_assistant)
        self.start_button.pack(side=tk.LEFT, padx=5)
        self.stop_button = tk.Button(self.control_frame, text="Stop Assistant", command=self.stop_assistant, state='disabled')
        self.stop_button.pack(side=tk.RIGHT, padx=5)

        self.assistant_running = False

    def log(self, text):
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, f"{text}\n")
        self.log_area.yview(tk.END)
        self.log_area.config(state='disabled')

    def send_command(self, event=None):
        command = self.command_entry.get()
        if command:
            self.log(f"You: {command}")
            response = process_command(command)
            self.log(f"Assistant: {response}")
            speak(response)
            self.command_entry.delete(0, tk.END)

    def start_assistant(self):
        self.log("Starting assistant...")
        self.assistant_running = True
        self.start_button.config(state='disabled')
        self.stop_button.config(state='normal')
        threading.Thread(target=self.run_assistant).start()

    def stop_assistant(self):
        self.log("Stopping assistant...")
        self.assistant_running = False
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')

    def run_assistant(self):
        while self.assistant_running:
            # Simulate listening for wake word (replace with actual wake word detection)
            # time.sleep(5)
            if wake_word_detection():
                self.log("Wake word detected!")
                command = listen()
                if command:  # Replace with actual command from speech
                    self.log(f"You: {command}")
                    response = process_command(command)
                    self.log(f"Assistant: {response}")
                    speak(response)


# Run the UI
if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceAssistantUI(root)
    root.mainloop()