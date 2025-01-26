import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

# Base URL of the forum
BASE_URL = "https://forum.universal-robots.com/c/technical-questions"

# Function to fetch and parse a single page
def fetch_page(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise exception for HTTP errors
        html = response.text
       # print(html)  # Add this to inspect the raw HTML
        return BeautifulSoup(html, "html.parser")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

# Step 1: Scrape topic URLs from the main page
def scrape_topic_urls(soup, max_topics=3):
    topic_urls = []
    links = soup.select("a.raw-topic-link")
    print(f"Found {len(links)} topics on the page.")

    for i, link in enumerate(links):
        if i >= max_topics:  # Limit the number of topics for testing
            break
        topic_url = link.attrs['href']
        
        # Check if the URL is relative or absolute
        if topic_url.startswith("http"):  # Absolute URL
            full_url = topic_url
        else:  # Relative URL
            full_url = f"https://forum.universal-robots.com{topic_url}"
        
        topic_urls.append(full_url)
        print(f"Scraped topic URL: {full_url}")

    return topic_urls


# Step 2: Scrape the main post and replies from a topic page
def scrape_topic(link):
    topic_data = {"title": None, "link": link, "post": None, "comments": []}
    soup = fetch_page(link)
    if soup is None:
        return None

    # Get the title of the topic
    title = soup.select_one("h1")
    if title:
        topic_data["title"] = title.text.strip()
     #   print(f"Title: {topic_data['title']}") this will print the title, useful for debugging
    else:
        print(f"Title not found for: {link}")

    # Get the main post content
    main_post = soup.select_one("div.post[itemprop='text']")
    if main_post:
        topic_data["post"] = main_post.text.strip()
    #    print(f"Main Post: {topic_data['post']}") this will print the post, useful for debugging
    else:
        print(f"Main post not found for: {link}")

    # Get the comments (replies)
    comments = soup.select("div[itemprop='comment'] div.post[itemprop='text']")
    for comment in comments:
        topic_data["comments"].append(comment.text.strip())
     #   print(f"Comment: {comment.text.strip()}") this will print the comments, useful for debugging

    return topic_data

# Function to handle scraping of both the main page and individual topics
def scrape_forum(start_url, max_pages=1, max_topics=3):
    all_topics = []
    url = start_url
    for page in range(1, max_pages + 1):
        print(f"Scraping page {page}: {url}")
        soup = fetch_page(url)
        if soup is None:
            print("Failed to fetch the page.")
            break

        # Step 1: Get topic URLs from the main page
        topic_urls = scrape_topic_urls(soup, max_topics=max_topics)

        # Step 2: Scrape each topic URL for details
        for topic_url in topic_urls:
            print(f"Scraping topic details from: {topic_url}")
            topic_data = scrape_topic(topic_url)
            if topic_data:
                all_topics.append(topic_data)

        # Check for next page (if applicable)
        next_page = soup.select_one("a[rel='next']")
        if next_page:
            url = f"https://forum.universal-robots.com{next_page['href']}"
        else:
            print("No more pages to scrape.")
            break

    return all_topics

# Save results to a JSON file
def save_to_json(data, filename_prefix="ur_forum_topics"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename_prefix}_{timestamp}.json"
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    print(f"Saved data to {filename}")

# Main script
if __name__ == "__main__":
    start_url = BASE_URL
    topics = scrape_forum(start_url, max_pages=1, max_topics=2)  # Limit to x pages and x topics, used for testing to limit the amount of data and avoid shadow banning
    print(f"Scraped {len(topics)} topics.")
    save_to_json(topics)
    print("Saved topics to JSON.")
