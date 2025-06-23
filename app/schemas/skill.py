from typing import Optional

from pydantic import BaseModel


class SkillBase(BaseModel):
    name: str
    category: str


class SkillCreate(SkillBase):
    pass


class SkillOut(SkillBase):
    id: int

    model_config = {
        "from_attributes": True
    }


class SkillUpdate(SkillBase):
    name: Optional[str]
    category: Optional[str]
