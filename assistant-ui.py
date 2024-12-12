import threading
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from datetime import datetime
import pyttsx3
import requests
import sqlite3
import webbrowser
import time
import re
import wikipedia
import random

# Dummy functions for testing (replace with actual ones from your code)
def speak(text):
    engine.say(text)
    engine.runAndWait()

def get_weather(city):
    # Dummy weather function
    return f"Weather in {city}: Sunny, 25°C."

def play_song(song_name):
    # Dummy song function
    return f"Playing song: {song_name}."

def process_command(command):
    # Example of handling commands
    if "weather" in command:
        city = re.search(r'weather in ([a-zA-Z\s]+)', command)
        if city:
            return get_weather(city.group(1))
        else:
            return "Please specify a city."
    elif "play" in command:
        song_name = command.replace("play", "").strip()
        return play_song(song_name)
    elif "time" in command:
        return f"The time is {datetime.now().strftime('%H:%M')}."
    elif "exit" in command:
        return "Goodbye!"
    else:
        return "I don't understand that command."

# Initialize pyttsx3
engine = pyttsx3.init()

# GUI Code
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
            time.sleep(5)
            if not self.assistant_running:
                break
            self.log("Wake word detected!")
            command = "play random song"  # Replace with actual command from speech
            self.log(f"You: {command}")
            response = process_command(command)
            self.log(f"Assistant: {response}")
            speak(response)


# Run the UI
if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceAssistantUI(root)
    root.mainloop()
