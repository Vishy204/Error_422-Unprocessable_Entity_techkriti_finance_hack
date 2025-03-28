import requests
from bs4 import BeautifulSoup
import json
import time
from transformers import pipeline

# Load Hugging Face Models
sentiment_model = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
ner_model = pipeline("ner", model="dslim/bert-base-NER")  # Named Entity Recognition

def extract_company_name(summary_text):
    """Extracts the company name from the financial summary using NER."""
    entities = ner_model(summary_text[:512])  # Limit to 512 tokens
    company_name = None

    for entity in entities:
        if entity["entity"] in ["B-ORG", "I-ORG"]:  # Organization name detected
            if company_name:
                company_name += " " + entity["word"]
            else:
                company_name = entity["word"]

    if company_name:
        company_name = company_name.replace(" ##", "")  # Remove sub-word tokens
        return company_name
    else:
        return "Reliance"  # No company name found

def get_financial_news_titles(company_name="reliance", max_results=30):
    """Fetches at least 30 financial news titles for a company and performs sentiment analysis."""
    
    search_query = company_name.replace(" ", "+") + "+financial+results+OR+earnings+OR+profit+OR+loss+OR+revenue"
    base_url = "https://www.google.com/search?q={query}&hl=en&tbm=nws&start={start}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    articles = []
    sentiment_score = 0  # Positive increases, negative decreases
    start = 0  # Start from the first page

    while len(articles) < max_results:
        url = base_url.format(query=search_query, start=start)
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"Failed to retrieve news (Page {start//10 + 1})")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.select(".SoaBEf")  # Google News articles

        if not results:
            print("No more news found.")
            break

        for result in results:
            title = result.select_one(".n0jPhd").text if result.select_one(".n0jPhd") else "No title"
            link = result.a["href"] if result.a else "No link"

            # Only consider news related to financial performance
            if any(keyword in title.lower() for keyword in ["profit", "loss", "revenue", "earnings", "financial", "quarterly"]):
                # Hugging Face Sentiment Analysis
                sentiment_result = sentiment_model(title)[0]
                sentiment = 1 if sentiment_result["label"] == "POSITIVE" else -1
                
                sentiment_score += sentiment  # Adjust sentiment score
                
                articles.append({
                    "title": title,
                    "link": link,
                    "sentiment": sentiment_result["label"],
                    "score": sentiment_result["score"]
                })

                if len(articles) >= max_results:
                    break

        start += 10  # Move to next page (Google News paginates every 10 results)
        time.sleep(1)  # Avoid rapid requests to prevent blocking

    return articles, sentiment_score

# Load Hugging Face Sentiment Analysis Model
sentiment_model = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

def analyze_financial_summary(summary_text):
    """Analyze sentiment of financial summary."""
    sentiment_result = sentiment_model(summary_text[:512])[0]  # Limit to 512 tokens (DistilBERT limit)
    sentiment = 1 if sentiment_result["label"] == "POSITIVE" else -1
    return sentiment, sentiment_result["score"]

def compare_sentiments(financial_summary, news_sentiment_score):
    """Compare financial summary sentiment with news sentiment."""
    
    summary_sentiment, summary_confidence = analyze_financial_summary(financial_summary)

    if summary_sentiment > 0 and news_sentiment_score > 0:
        return f"✅ The company's performance aligns with public perception. (Confidence: {summary_confidence:.2f})"
    elif summary_sentiment < 0 and news_sentiment_score < 0:
        return f"✅ The company's struggles are accurately reflected in public news. (Confidence: {summary_confidence:.2f})"
    else:
        return f"⚠️ The company's public financial perception does not match its actual performance! (Confidence: {summary_confidence:.2f})"