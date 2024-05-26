# app/utility.py

import openai
import os
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import crud, models
import threading
from concurrent.futures import ThreadPoolExecutor

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Define a semaphore to limit the number of concurrent threads
semaphore = threading.Semaphore(5)  # Adjust the number as needed

def generate_content(db: Session, topic: str) -> str:
    with semaphore:
        search_term = crud.get_search_term(db, topic)
        if not search_term:
            search_term = crud.create_search_term(db, topic)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Write a detailed article about {topic}"},
            ]
        )
        generated_text = response.choices[0].message['content'].strip()
        crud.create_generated_content(db, generated_text, search_term.id)
        return generated_text

def analyze_content(db: Session, content: str):
    with semaphore:
        search_term = crud.get_search_term(db, content)
        if not search_term:
            search_term = crud.create_search_term(db, content)
        readability = get_readability_score(content)
        sentiment = get_sentiment_analysis(content)
        crud.create_sentiment_analysis(db, readability, sentiment, search_term.id)
        return readability, sentiment

def get_readability_score(content: str) -> str:
    # Simulate readability score for the example
    # Replace this with actual readability API call if available
    return "Readability Score: Good"

def get_sentiment_analysis(content: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Analyze the sentiment of the following text:\n\n{content}\n\nIs the sentiment positive, negative, or neutral?"},
        ],
        max_tokens=10
    )
    return response.choices[0].message['content'].strip()
