import json
import re
import nltk
import yake
import pandas as pd
import os
import glob
from rake_nltk import Rake
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter
from nltk.corpus import stopwords

# Ensure required NLTK resources are available
nltk.download("stopwords")
nltk.download("punkt")

# Load English stopwords
STOPWORDS = set(stopwords.words("english"))

# Function to find the latest JSON file in the directory
def get_latest_json():
    json_files = glob.glob("*.json")  # Find all JSON files in the directory
    if not json_files:
        raise FileNotFoundError("No JSON files found in the current directory.")

    latest_file = max(json_files, key=os.path.getctime)  # Get the most recently created file
    print(f"Using JSON file: {latest_file}")  # Debugging info
    return latest_file

# Function to load JSON data
def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

# Function to clean and preprocess text
def clean_text(text):
    if not text:
        return ""
    text = text.lower()  # Convert to lowercase
    text = re.sub(r"\W+", " ", text)  # Remove non-word characters
    text = " ".join([word for word in text.split() if word not in STOPWORDS])  # Remove stopwords
    return text

# Extract keywords using TF-IDF
def extract_tfidf_keywords(texts, num_keywords=10):
    vectorizer = TfidfVectorizer(max_features=500, stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(texts)
    feature_names = vectorizer.get_feature_names_out()
    summed_tfidf = tfidf_matrix.sum(axis=0)
    scores = [(feature_names[i], summed_tfidf[0, i]) for i in range(len(feature_names))]
    sorted_keywords = sorted(scores, key=lambda x: x[1], reverse=True)[:num_keywords]
    return [keyword[0] for keyword in sorted_keywords]

# Extract keywords using YAKE
def extract_yake_keywords(text, num_keywords=10):
    kw_extractor = yake.KeywordExtractor(n=1, top=num_keywords)
    keywords = kw_extractor.extract_keywords(text)
    return [kw[0] for kw in keywords]

# Extract keywords using RAKE
def extract_rake_keywords(text, num_keywords=10):
    rake = Rake(stopwords=STOPWORDS)
    rake.extract_keywords_from_text(text)
    return rake.get_ranked_phrases()[:num_keywords]

# Process the JSON file and extract keywords
def process_json(input_file, output_file):
    data = load_json(input_file)

    all_texts = []
    results = []

    for topic in data:
        title = topic.get("title", "")
        post = topic.get("post", "")
        comments = " ".join(topic.get("comments", []))

        combined_text = f"{title} {post} {comments}"
        cleaned_text = clean_text(combined_text)
        all_texts.append(cleaned_text)

        keywords_tfidf = extract_tfidf_keywords([cleaned_text], num_keywords=10)
        keywords_yake = extract_yake_keywords(cleaned_text, num_keywords=10)
        keywords_rake = extract_rake_keywords(cleaned_text, num_keywords=10)

        results.append({
            "title": title,
            "link": topic.get("link", ""),
            "tfidf_keywords": keywords_tfidf,
            "yake_keywords": keywords_yake,
            "rake_keywords": keywords_rake
        })

    # Save the results to JSON
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=4, ensure_ascii=False)

    print(f"Keyword extraction complete. Results saved to {output_file}")

# Run the script
if __name__ == "__main__":
    input_file = get_latest_json()  # Automatically find the latest JSON file
    output_file = "keywords_output.json"
    process_json(input_file, output_file)
