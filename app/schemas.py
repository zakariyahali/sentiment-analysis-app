# app/schemas.py

from pydantic import BaseModel

class GeneratePayload(BaseModel):
    topic: str

class AnalyzePayload(BaseModel):
    content: str

class SearchTermBase(BaseModel):
    term: str

class SearchTermCreate(SearchTermBase):
    pass

class SearchTerm(SearchTermBase):
    id: int
    class Config:
        orm_mode: True

class GeneratedContentBase(BaseModel):
    content: str

class GeneratedContentCreate(GeneratedContentBase):
    search_term_id: int

class GeneratedContent(GeneratedContentBase):
    id: int
    search_term_id: int
    class Config:
        orm_mode: True

class SentimentAnalysisBase(BaseModel):
    readability: str
    sentiment: str

class SentimentAnalysisCreate(SentimentAnalysisBase):
    search_term_id: int

class SentimentAnalysis(SentimentAnalysisBase):
    id: int
    search_term_id: int
    class Config:
        orm_mode: True
