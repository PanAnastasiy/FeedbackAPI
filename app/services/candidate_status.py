from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.candidate_status import CandidateStatusRepository
from app.schemas.candidate_status import CandidateStatusCreate, CandidateStatusUpdate
from app.models.candidate_status import CandidateStatus
from app.services.base import BaseService


class CandidateStatusService(BaseService[CandidateStatus, CandidateStatusCreate, CandidateStatusUpdate]):
    def __init__(self, db: AsyncSession):
        super().__init__(CandidateStatusRepository(db))
