from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


# ── Request body (what the frontend sends)
class ContactCreate(BaseModel):
    name:    str      = Field(..., min_length=2,  max_length=120,  example="John Doe")
    email:   EmailStr = Field(...,                                  example="john@example.com")
    subject: str      = Field(..., min_length=3,  max_length=255,  example="Collaboration Offer")
    message: str      = Field(..., min_length=10, max_length=5000, example="Hi Ahmed, I'd like to...")

    model_config = {"str_strip_whitespace": True}


# ── Response after successful submission
class ContactResponse(BaseModel):
    success: bool
    id:      int
    detail:  str


# ── Used by the /messages admin endpoint
class MessageOut(BaseModel):
    id:      int
    name:    str
    email:   str
    subject: str
    message: str
    sent_at: datetime

    model_config = {"from_attributes": True}
