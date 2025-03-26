import json
import os
import requests
from bs4 import BeautifulSoup
import logging

# Logging Configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_latest_news():
    url = "https://www.ndtv.com/latest"
    headers = {"User-Agent": "Mozilla/5.0"}  
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()     #   HTTP errors check krne k liye
    except requests.RequestException as e:
        logging.error(f"Request failed: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    news_list = []

    for article in soup.find_all('h2', class_='NwsLstPg_ttl'):
        link = article.find('a', href=True)
        if link and link.text.strip():
            news_list.append({
                "headline": link.text.strip()
            })

    if not news_list:
        logging.warning("No news articles found.")
    else:
        logging.info(f"{len(news_list)} headlines scraped successfully.")

    return news_list

# JSON File me Save Karna
def save_news_to_json():
    news = get_latest_news()
    if not news:
        logging.warning("No news to save.")
        return
    
    file_path = os.path.join(os.path.dirname(__file__), "latest_news.json")
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(news, f, indent=4, ensure_ascii=False)
        logging.info(f"News data saved successfully to {file_path}")
    except IOError as e:
        logging.error(f"Failed to save news data: {e}")

if __name__ == "__main__":
    save_news_to_json()
