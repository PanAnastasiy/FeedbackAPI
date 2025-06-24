from sqlalchemy import Column, Integer, String

from app.db.base import Base


class FeedbackSection(Base):
    __tablename__ = 'feedback_sections'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
