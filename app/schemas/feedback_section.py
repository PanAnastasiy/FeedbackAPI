from pydantic import BaseModel
from typing import Optional


class FeedbackSectionBase(BaseModel):
    name: str
    description: Optional[str] = None


class FeedbackSectionCreate(FeedbackSectionBase):
    pass


class FeedbackSectionUpdate(FeedbackSectionBase):
    name: Optional[str] = None


class FeedbackSectionOut(FeedbackSectionBase):
    id: int

    model_config = {
        "from_attributes": True
    }
