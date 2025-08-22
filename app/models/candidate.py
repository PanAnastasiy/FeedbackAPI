from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship


from app.db.base import Base


class Candidate(Base):
    __tablename__ = 'candidates'
    id = Column(Integer, primary_key=True)
    fullname = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    position = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)
    status_id = Column(Integer, ForeignKey('candidate_statuses.id'))
    status_obj = relationship('CandidateStatus', back_populates="candidates")
