# app/utility.py

import openai
import requests
import threading
from fastapi import BackgroundTasks
from sqlalchemy.orm import Session
import crud

# Load environment variables
import os
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_content(topic: str) -> str:
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Write a detailed article about {topic}",
        max_tokens=500
    )
    return response.choices[0].text.strip()

def analyze_content(db: Session, content: str):
    readability = get_readability_score(content)
    sentiment = get_sentiment_analysis(content)

    content_id = crud.create_generated_content(db, content).id
    crud.create_analysis_result(db, content_id, readability, sentiment)

def get_readability_score(content: str) -> str:
    response = requests.post("https://readability-api.example.com", data={"text": content})
    return response.json().get("readability_score", "N/A")

def get_sentiment_analysis(content: str) -> str:
    response = requests.post("https://sentiment-api.example.com", data={"text": content})
    return response.json().get("sentiment", "N/A")

# Multithreading with semaphore
thread_limit = threading.Semaphore(5)  # Limit to 5 concurrent threads

def threaded_analysis(db: Session, content: str):
    with thread_limit:
        analyze_content(db, content)

def analyze_twitter_sentiment(db: Session, term: str):
    tweets = crud.get_tweets_by_term(db, term)
    sentiments = [get_sentiment_analysis(tweet.tweet) for tweet in tweets]
    # Store or return aggregated sentiment analysis results as needed
    # Here we can just print the sentiments or store them in the database
    print(f"Sentiments for term '{term}': {sentiments}")








