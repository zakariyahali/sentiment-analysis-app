# app/main.py

from fastapi import FastAPI, Request, Depends, BackgroundTasks
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import models, crud, database, utility, twitter_scraper, schemas
from database import engine, SessionLocal
from pydantic import BaseModel

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

class GeneratePayload(BaseModel):
    topic: str

@app.post("/generate/")
async def generate_and_analyze(payload: GeneratePayload, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    generated_text = utility.generate_content(payload.topic)
    background_tasks.add_task(utility.analyze_content, db, generated_text)
    return {"generated_text": generated_text}
