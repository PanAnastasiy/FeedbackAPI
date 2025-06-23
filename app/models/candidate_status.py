from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class CandidateStatus(Base):
    __tablename__ = 'candidate_statuses'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    # Обратная связь с кандидатами
    candidates = relationship('Candidate', back_populates="status_obj")
