from typing import Optional

from pydantic import BaseModel


class CandidateStatusBase(BaseModel):
    name: str


class CandidateStatusCreate(CandidateStatusBase):
    pass


class CandidateStatusUpdate(CandidateStatusBase):
    name: Optional[str]


class CandidateStatusOut(CandidateStatusBase):
    id: int

    model_config = {
        "from_attributes": True  # вместо orm_mode = True
    }
