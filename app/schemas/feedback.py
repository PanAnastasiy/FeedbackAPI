from pydantic import BaseModel


class FeedbackRequest(BaseModel):
    keywords: list[str]