# Universal Robots Forum Scraper & Keyword Extractor

This project consists of a web scraper and keyword extractor designed to analyze discussions from the Universal Robots forum. The scraper collects forum posts, while the extractor processes them to generate AI-driven keywords using multiple techniques.

### Overview of the Process

## Web Scrapin
- The scraper collects data from the Universal Robots forum, retrieving:
 - Titles of discussion topics.
 - Main post content.
 - User comments on each topic.
- The scraped data is saved in a JSON file for further processing.

## Keyword Extraction
- The extracted forum data is processed to generate relevant keywords using three different techniques:
 - TF-IDF (Term Frequency-Inverse Document Frequency) – Identifies the most statistically important words.
 - YAKE (Yet Another Keyword Extractor) – Extracts keywords from individual documents using statistical patterns.
 - RAKE (Rapid Automatic Keyword Extraction) – Detects multi-word phrases based on word co-occurrence.
- The extracted keywords are saved in a new JSON file for easy analysis.

## Prerequisites
Ensure you have **Python 3.12+** installed.

### Install Required Libraries
Run the following command in your terminal or command prompt:

> pip install requests beautifulsoup4 nltk yake rake-nltk scikit-learn pandas

#### In some cases, you may need to manually download stopwords and punkt for NLTK. To do this:

Open Python in your terminal:

> python3.12
> import nltk
> nltk.download("stopwords")
> nltk.download("punkt")
> exit()

# How to Use the Scraper & Extractor

## Step 1: Run the Web Scraper
 - run the scraper.py script

 The script scrapes forum topics and saves them in a JSON file.
 The output file will be automatically named based on the timestamp.

## Step 2: Run the Keyword Extraction Script
 - run the keyword_extraction.py script

 This script reads the latest scraped JSON file.

 It applies TF-IDF, YAKE, and RAKE to extract important keywords.

 Saves the output in keywords_output.json.


## Common Issues & Fixes
#### Issue: FileNotFoundError
Ensure the scraper has run before executing the keyword extraction script.
Check if the JSON file exists in the directory.

#### Issue: LookupError: Resource punkt_tab not found
Run nltk.download("punkt") manually inside Python as explained above.

#### Issue: ModuleNotFoundError: No module named 'rake_nltk'
Run pip install rake-nltk to install the missing dependency.


## Output Example

### Extracted Keywords JSON Format

{
    "topics": [
        {
            "title": "Remote TCP & Toolpath fails to start in UR simulator",
            "link": "https://forum.universal-robots.com/t/remote-tcp-toolpath-fails-to-start-in-ur-simulator/37757",
            "tfidf_keywords": ["urcap", "remote", "start", "tcp"],
            "yake_keywords": ["tcp", "toolpath", "version"],
            "rake_keywords": ["remote tcp toolpath fails start ur simulator"]
        }
    ],
    "summary": {
        "total_tfidf_keywords": {"robot": 5, "control": 3},
        "total_yake_keywords": {"robot": 6, "program": 4},
        "total_rake_keywords": {"technical questions category": 3},
        "total_combined_keywords_filtered": {"robot": 10, "program": 7}
    }
}
