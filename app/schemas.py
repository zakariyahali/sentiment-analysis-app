# app/schemas.py

from pydantic import BaseModel

class GeneratePayload(BaseModel):
    topic: str
