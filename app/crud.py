# app/crud.py

from sqlalchemy.orm import Session
import models

def create_generated_content(db: Session, content: str):
    db_content = models.Content(text=content)
    db.add(db_content)
    db.commit()
    db.refresh(db_content)
    return db_content

def create_analysis_result(db: Session, content_id: int, readability: str, sentiment: str, seo: str):
    db_result = models.AnalysisResult(content_id=content_id, readability=readability, sentiment=sentiment, seo=seo)
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result

def create_tweet(db: Session, term: str, tweet: str):
    db_tweet = models.Tweet(term=term, tweet=tweet)
    db.add(db_tweet)
    db.commit()
    db.refresh(db_tweet)
    return db_tweet

def get_tweets_by_term(db: Session, term: str):
    return db.query(models.Tweet).filter(models.Tweet.term == term).all()
