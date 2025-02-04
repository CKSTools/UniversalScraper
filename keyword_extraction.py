import json
import re
import nltk
import yake
import os
import glob
from rake_nltk import Rake
from collections import Counter
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

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

# Function to count keyword occurrences
def count_keywords(keyword_lists):
    word_counter = Counter()
    for keywords in keyword_lists:
        word_counter.update(keywords)
    return dict(word_counter)

# Function to remove keywords that appear only once and sort them
def filter_and_sort_keywords(keyword_counts):
    filtered_counts = {word: count for word, count in keyword_counts.items() if count > 1}
    sorted_counts = dict(sorted(filtered_counts.items(), key=lambda item: item[1], reverse=True))
    return sorted_counts

# Process the JSON file and extract keywords
def process_json(input_file, output_file):
    data = load_json(input_file)

    all_texts = []

    tfidf_all_keywords = []
    yake_all_keywords = []
    rake_all_keywords = []

    for topic in data:
        title = topic.get("title", "")
        post = topic.get("post", "")
        comments = " ".join(topic.get("comments", []))

        combined_text = f"{title} {post} {comments}"
        cleaned_text = clean_text(combined_text)
        all_texts.append(cleaned_text)

        # Extract keywords
        keywords_tfidf = extract_tfidf_keywords([cleaned_text], num_keywords=10)
        keywords_yake = extract_yake_keywords(cleaned_text, num_keywords=10)
        keywords_rake = extract_rake_keywords(cleaned_text, num_keywords=10)

        # Store keywords for total count
        tfidf_all_keywords.extend(keywords_tfidf)
        yake_all_keywords.extend(keywords_yake)
        rake_all_keywords.extend(keywords_rake)

        # COMMENTED OUT: Individual topic keyword storage
        # results.append({
        #     "title": title,
        #     "link": topic.get("link", ""),
        #     "tfidf_keywords": keywords_tfidf,
        #     "yake_keywords": keywords_yake,
        #     "rake_keywords": keywords_rake
        # })

    # Compute total counts and filter out keywords appearing only once
    tfidf_counts_filtered = filter_and_sort_keywords(count_keywords([tfidf_all_keywords]))
    yake_counts_filtered = filter_and_sort_keywords(count_keywords([yake_all_keywords]))
    rake_counts_filtered = filter_and_sort_keywords(count_keywords([rake_all_keywords]))

    # Combine all keyword occurrences into a single count and filter them
    total_keyword_counts = count_keywords([tfidf_all_keywords, yake_all_keywords, rake_all_keywords])
    filtered_sorted_total_keyword_counts = filter_and_sort_keywords(total_keyword_counts)

    # Save only the summary results
    summary_results = {
        "total_tfidf_keywords": tfidf_counts_filtered,
        "total_yake_keywords": yake_counts_filtered,
        "total_rake_keywords": rake_counts_filtered,
        "total_combined_keywords_filtered": filtered_sorted_total_keyword_counts  # Words with count > 1, sorted
    }

    # Save the results to JSON
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(summary_results, file, indent=4, ensure_ascii=False)

    print(f"Keyword extraction complete. Summary results saved to {output_file}")

# Run the script
if __name__ == "__main__":
    input_file = get_latest_json()  # Automatically find the latest JSON file
    output_file = "keywords_summary.json"
    process_json(input_file, output_file)
