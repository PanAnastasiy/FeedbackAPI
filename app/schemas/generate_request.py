from pydantic import BaseModel


from typing import List
from pydantic import BaseModel


class SkillInput(BaseModel):
    name: str
    level: int


class GenerateRequest(BaseModel):
    section_name: str
    keywords: str
    skills: List[SkillInput] = []
