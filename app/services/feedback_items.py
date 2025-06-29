from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.feedback_item import FeedbackItem
from app.repositories.feedback_item import FeedbackItemRepository
from app.schemas.feedback_item import FeedbackItemCreate, FeedbackItemUpdate
from app.services.base import BaseService


class FeedbackItemService(BaseService[FeedbackItem, FeedbackItemCreate, FeedbackItemUpdate]):
    def __init__(self, db: AsyncSession):
        super().__init__(FeedbackItemRepository(db))