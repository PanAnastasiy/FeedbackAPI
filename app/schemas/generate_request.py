from pydantic import BaseModel


class GenerateRequest(BaseModel):
    section_name: str
    keywords: str
