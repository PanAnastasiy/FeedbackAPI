from sqlalchemy.ext.asyncio import AsyncSession

from app.models.feedback_item import FeedbackItem
from app.repositories.base import BaseRepository
from app.schemas.feedback_item import FeedbackItemCreate, FeedbackItemOut, FeedbackItemUpdate


class FeedbackItemRepository(BaseRepository[
    FeedbackItem, FeedbackItemCreate, FeedbackItemUpdate, FeedbackItemOut
]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db, FeedbackItem, FeedbackItemOut)

