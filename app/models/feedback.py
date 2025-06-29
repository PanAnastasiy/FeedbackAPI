from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.base import Base


class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    interviewer_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    final_feedback = Column(Text)

    items = relationship("FeedbackItem", back_populates="feedback", cascade="all, delete")
