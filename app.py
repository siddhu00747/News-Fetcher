import subprocess
import os
import json
from flask import Flask, render_template, jsonify

app = Flask(__name__)

def run_news_scraper():
    try:
        print("Fetching latest news using news_scraper.py...")
        result = subprocess.run(['python', 'news_scraper.py'], capture_output=True, text=True)
        if result.returncode != 0:
            print("Error running news_scraper.py:", result.stderr)
            return False
        print(result.stdout)
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

@app.route('/news')
def get_news():
    if not run_news_scraper():
        return jsonify({"error": "Failed to fetch latest news."})

    if not os.path.isfile('latest_news.json'):
        return jsonify({"error": "latest_news.json not found."})

    with open('latest_news.json', 'r', encoding='utf-8') as file:
        try:
            news_data = json.load(file)
            headlines = [news["headline"] for news in news_data]
            return jsonify(headlines)
        except json.JSONDecodeError:
            return jsonify({"error": "Invalid JSON data."})

@app.route('/')
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
