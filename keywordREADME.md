# Universal Robots Forum Scraper & Keyword Extractor

This project consists of a web scraper and keyword extractor for analyzing discussion topics from the Universal Robots forum. The scraper collects forum posts, and the extractor processes them to generate keywords using various AI-powered techniques.

## Features
- Scrapes forum topics, including titles, posts, and comments.
- Extracts keywords using **TF-IDF**, **YAKE**, and **RAKE**.
- Saves extracted keywords in a JSON file for further analysis.

## Prerequisites

Ensure you have **Python 3.12+** installed.

### Install Required Libraries
Run the following command in your terminal or command prompt:


#### In some cases, you may need to manually download stopwords and punkt for NLTK. To do this:

Open Python in your terminal:

> python3.12
> import nltk
> nltk.download("stopwords")
> nltk.download("punkt")
> exit()


#### Common Issues & Fixes
Issue: FileNotFoundError
Ensure the scraper has run before executing the keyword extraction script.
Check if the JSON file exists in the directory.

Issue: LookupError: Resource punkt_tab not found
Run nltk.download("punkt") manually inside Python as explained above.

Issue: ModuleNotFoundError: No module named 'rake_nltk'
Run pip install rake-nltk to install the missing dependency.
