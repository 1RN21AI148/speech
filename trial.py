from flask import Flask, request, jsonify
import sqlite3
import requests
import wikipedia
from datetime import datetime
import random

app = Flask(__name__)

# API Keys and base URLs for external services
WEATHER_API_KEY = "df609a094fb3e0f3de0caf4c8265c2a5"
NEWS_API_KEY = "pub_57529749d229a820456ae31d1b3a5985783a4"
WEATHER_BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
NEWS_URL = f"https://newsdata.io/api/1/latest?apikey={NEWS_API_KEY}&country=in&prioritydomain=top"



@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "City not specified"}), 400

    try:
        url = f"{WEATHER_BASE_URL}?q={city}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url)
        weather_data = response.json()

        if weather_data["cod"] != "404":
            main = weather_data['main']
            description = weather_data['weather'][0]['description']
            report = f"The temperature in {city} is {main['temp']}°C with {description}. Humidity is {main['humidity']}%."
            return jsonify({"weather_report": report})
        else:
            return jsonify({"error": "City not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/news', methods=['GET'])
def get_news_headlines():
    try:
        response = requests.get(NEWS_URL)
        newsdata_response = response.json()
        
        if newsdata_response.get("status") == "success" and newsdata_response.get("results"):
            articles = newsdata_response["results"][:5]
            headlines = [article["title"] for article in articles]
            return jsonify({"headlines": headlines})
        else:
            return jsonify({"error": "No articles found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/wikipedia', methods=['GET'])
def get_wikipedia_summary():
    subject = request.args.get('subject')
    if not subject:
        return jsonify({"error": "Subject not specified"}), 400
    
    try:
        summary = wikipedia.summary(subject, sentences=2)
        return jsonify({"summary": summary})
    except wikipedia.exceptions.PageError:
        return jsonify({"error": "No Wikipedia page found"}), 404
    except wikipedia.exceptions.DisambiguationError:
        return jsonify({"error": "Multiple results found, please be more specific"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500



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

@app.route('/songs/<genre>', methods=['GET'])
def get_songs_by_genre(genre):
    conn = sqlite3.connect('songs.db')
    cursor = conn.cursor()
    cursor.execute('SELECT song_name, path FROM songs WHERE genre = ?', (genre,))
    songs = cursor.fetchall()
    conn.close()

    if songs:
        return jsonify({"songs": songs})
    else:
        return jsonify({"error": "No songs found for this genre"}), 404



if __name__ == '__main__':
    setup_database()  # Set up the database tables if not already created
    app.run(host='0.0.0.0', port=5000, debug=True)




