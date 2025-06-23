from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Candidate
from app.repositories.candidate import CandidateRepository
from app.repositories.candidate_status import CandidateStatusRepository
from app.schemas.candidate import CandidateCreate, CandidateUpdate
from app.services.base import BaseService


class CandidateService(BaseService[Candidate, CandidateCreate, CandidateUpdate]):
    def __init__(self, db: AsyncSession):
        super().__init__(CandidateRepository(db))
        self.status_repo = CandidateStatusRepository(db)

    async def create(self, obj_in: CandidateCreate) -> Candidate:
        data = obj_in.model_dump(exclude_unset=True)
        status_name = data.pop("status", None)

        if status_name:
            status_obj = await self.status_repo.get_by_name(status_name)
            if not status_obj:
                raise ValueError(f"Статус '{status_name}' не найден.")
            data["status_id"] = status_obj.id

        return await self.repository.create_raw(data)

    async def update(self, obj_id: int, obj_in: CandidateUpdate) -> Optional[Candidate]:
        data = obj_in.model_dump(exclude_unset=True)
        status_name = data.pop("status", None)

        if status_name is not None:
            status_obj = await self.status_repo.get_by_name(status_name)
            if not status_obj:
                raise ValueError(f"Статус '{status_name}' не найден.")
            data["status_id"] = status_obj.id

        return await self.repository.update_raw(obj_id, data)
