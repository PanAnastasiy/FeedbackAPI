# schemas.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


# --- FeedbackItem Schemas ---
class FeedbackItemBase(BaseModel):
    section_id: int
    skill_id: int
    level: Optional[int] = None
    comment: Optional[str] = None


class FeedbackItemCreate(FeedbackItemBase):
    pass


class FeedbackItemUpdate(BaseModel):
    section_id: int
    skill_id: int
    level: Optional[int] = None
    comment: Optional[str] = None


class FeedbackItemOut(FeedbackItemBase):
    id: int

    model_config = {
        "from_attributes": True  # вместо orm_mode = True
    }
