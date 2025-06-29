from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from app.schemas.feedback_item import FeedbackItemCreate, FeedbackItemOut, FeedbackItemUpdate


# --- Feedback Schemas ---
class FeedbackBase(BaseModel):
    candidate_id: int
    final_feedback: str


class FeedbackCreate(FeedbackBase):
    items: List[FeedbackItemCreate]


class FeedbackUpdate(BaseModel):
    final_feedback: Optional[str] = None
    items: Optional[List[FeedbackItemUpdate]] = None


class FeedbackOut(FeedbackBase):
    id: int
    interviewer_id: int
    created_at: datetime
    items: List[FeedbackItemOut]

    model_config = {
        "from_attributes": True  # вместо orm_mode = True
    }
