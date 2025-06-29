from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.feedback import Feedback
from app.repositories.feedback import FeedbackRepository
from app.schemas.feedback import FeedbackCreate, FeedbackUpdate
from app.services.base import BaseService


class FeedbackService(BaseService[Feedback, FeedbackCreate, FeedbackUpdate]):
    def __init__(self, db: AsyncSession):
        super().__init__(FeedbackRepository(db))

    async def create(self, obj_in: FeedbackCreate, interviewer_id: int = 1) -> Feedback:
        data = obj_in.model_dump()
        data["interviewer_id"] = interviewer_id
        return await self.repository.create_raw(data)

    async def update(self, obj_id: int, obj_in: FeedbackUpdate) -> Optional[Feedback]:
        data = obj_in.model_dump(exclude_unset=True)
        return await self.repository.update_raw(obj_id, data)
