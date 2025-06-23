
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Candidate
from app.repositories.base import BaseRepository
from app.schemas.candidate import CandidateOut, CandidateCreate, CandidateUpdate


class CandidateRepository(BaseRepository[
    Candidate, CandidateCreate, CandidateUpdate, CandidateOut
]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Candidate, CandidateOut)
