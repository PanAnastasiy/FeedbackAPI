from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, computed_field

from app.schemas.candidate_status import CandidateStatusOut


class CandidateBase(BaseModel):
    fullname: str
    email: str
    position: str
    status: Optional[str] = None  # Изменено на строку


class CandidateCreate(CandidateBase):
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    model_config = {
        "from_attributes": True
    }


class CandidateOut(BaseModel):
    id: int
    fullname: str
    email: str
    position: str
    created_at: Optional[datetime]
    status_obj: Optional[CandidateStatusOut] = Field(None, exclude=True)

    @computed_field
    @property
    def status(self) -> Optional[str]:
        return self.status_obj.name if self.status_obj else None

    model_config = {
        "from_attributes": True,
        "populate_by_name": True
    }


class CandidateUpdate(CandidateBase):
    fullname: Optional[str] = None
    email: Optional[str] = None
    position: Optional[str] = None
    status: Optional[str] = None
