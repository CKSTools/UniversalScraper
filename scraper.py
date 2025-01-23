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

# Function to scrape details of a single topic
def scrape_topic(link):
    topic_data = {"title": None, "link": link, "post": None, "comments": []}
    soup = fetch_page(link)
    if soup is None:
        return None

    # Get the title of the topic
    title = soup.select_one("a.fancy-title")
    if title:
        topic_data["title"] = title.text.strip()
        print(f"Title: {topic_data['title']}")
    else:
        print("Title not found.")

    # Get the main post content
    main_post = soup.select_one(".topic-post .cooked")
    if main_post:
        topic_data["post"] = main_post.text.strip()
        print(f"Post: {topic_data['post']}")
    else:
        print("Main post not found.")

    # Get comments/replies
    replies = soup.select(".timeline-container .topic-post .cooked")
    for reply in replies:
        comment = reply.text.strip()
        topic_data["comments"].append(comment)
        print(f"Comment: {comment}")

    return topic_data

# Function to scrape topics from a single page
def scrape_topics(soup, max_topics=3):
    topics = []
    links = soup.select("a.raw-topic-link")
    print(f"Found {len(links)} topics on the page.")

    for i, link in enumerate(links):
        if i >= max_topics:  # Stop after scraping the specified number of topics
            break

        topic_link = link.attrs['href']
        print(f"Scraping topic: {topic_link}")
        topic_data = scrape_topic(topic_link)
        if topic_data:
            topics.append(topic_data)

    return topics

# Function to handle pagination and scrape multiple pages
def scrape_forum(start_url, max_pages=1, max_topics=3):
    all_topics = []
    url = start_url
    for page in range(1, max_pages + 1):
        print(f"Scraping page {page}: {url}")
        soup = fetch_page(url)
        if soup is None:
            print("Failed to fetch the page.")
            break

        topics = scrape_topics(soup, max_topics=max_topics)
        print(f"Scraped {len(topics)} topics from page {page}.")
        all_topics.extend(topics)
        break  # Stop after processing the first page for this test

    return all_topics

# Save results to a CSV file
def save_to_csv(data, filename="ur_forum_topics.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        fieldnames = ["title", "link", "post", "comments"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for topic in data:
            writer.writerow({
                "title": topic["title"],
                "link": topic["link"],
                "post": topic["post"],
                "comments": " | ".join(topic["comments"])  # Join comments with a separator
            })

# Main script
if __name__ == "__main__":
    start_url = BASE_URL
    topics = scrape_forum(start_url, max_pages=1, max_topics=3)  # Scrape only 3 topics
    print(f"Scraped {len(topics)} topics.")
    save_to_csv(topics)
    print("Saved topics to ur_forum_topics.csv")
