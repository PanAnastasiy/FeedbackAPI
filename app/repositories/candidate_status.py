from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.candidate_status import CandidateStatus
from app.repositories.base import BaseRepository
from app.schemas.candidate_status import CandidateStatusOut, CandidateStatusCreate, CandidateStatusUpdate


class CandidateStatusRepository(BaseRepository[
    CandidateStatus, CandidateStatusCreate, CandidateStatusUpdate, CandidateStatusOut
]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, CandidateStatus, CandidateStatusOut)

    async def get_by_name(self, name: str) -> CandidateStatus | None:
        stmt = select(CandidateStatus).where(CandidateStatus.name == name)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
