import requests
from bs4 import BeautifulSoup
import csv
import time

# Base URL of the forum
BASE_URL = "https://forum.universal-robots.com/c/technical-questions"

# Function to fetch and parse a single page
def fetch_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for HTTP errors
        return BeautifulSoup(response.text, "html.parser")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

# Function to scrape topics from a single page
def scrape_topics(soup):
    topics = []
    for topic in soup.select("div.topic-title"):
        title = topic.get_text(strip=True)
        link = topic.find("a")["href"]
        full_link = f"https://forum.universal-robots.com{link}"
        topics.append({"title": title, "link": full_link})
    return topics

# Function to handle pagination and scrape multiple pages
def scrape_forum(start_url, max_pages=5):
    all_topics = []
    url = start_url
    for page in range(1, max_pages + 1):
        print(f"Scraping page {page}: {url}")
        soup = fetch_page(url)
        if soup is None:
            break
        topics = scrape_topics(soup)
        all_topics.extend(topics)

        # Find the "next page" link
        next_page = soup.select_one("a.next")
        if not next_page:
            break
        url = f"https://forum.universal-robots.com{next_page['href']}"
        time.sleep(2)  # Be polite and avoid rapid requests
    return all_topics

# Save results to a CSV file
def save_to_csv(data, filename="ur_forum_topics.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["title", "link"])
        writer.writeheader()
        writer.writerows(data)

# Main script
if __name__ == "__main__":
    start_url = BASE_URL
    topics = scrape_forum(start_url, max_pages=10)
    print(f"Scraped {len(topics)} topics.")
    save_to_csv(topics)
    print("Saved topics to ur_forum_topics.csv")