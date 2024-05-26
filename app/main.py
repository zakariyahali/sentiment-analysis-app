# app/main.py

from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import models, crud, database, utility, schemas
from database import engine, SessionLocal
from starlette.concurrency import run_in_threadpool

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

@app.post("/generate/")
async def generate_content(payload: schemas.GeneratePayload, db: Session = Depends(get_db)):
    generated_text = await run_in_threadpool(utility.generate_content, db, payload.topic)
    return {"generated_text": generated_text}

@app.post("/analyze/")
async def analyze_content(payload: schemas.AnalyzePayload, db: Session = Depends(get_db)):
    readability, sentiment = await run_in_threadpool(utility.analyze_content, db, payload.content)
    return {"readability": readability, "sentiment": sentiment}
