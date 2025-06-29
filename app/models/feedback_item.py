from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.db.base import Base


class FeedbackItem(Base):
    __tablename__ = "feedback_items"

    id = Column(Integer, primary_key=True, index=True)
    feedback_id = Column(Integer, ForeignKey("feedbacks.id"))
    section_id = Column(Integer, ForeignKey("feedback_sections.id"))
    skill_id = Column(Integer, ForeignKey("skills.id"))
    level = Column(Integer)
    comment = Column(Text)
    feedback = relationship("Feedback", back_populates="items")
