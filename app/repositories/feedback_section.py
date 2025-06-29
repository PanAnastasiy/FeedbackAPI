from sqlalchemy.ext.asyncio import AsyncSession

from app.models.feedback_section import FeedbackSection
from app.repositories.base import BaseRepository
from app.schemas.feedback_section import FeedbackSectionCreate, FeedbackSectionUpdate, FeedbackSectionOut


class FeedbackSectionRepository(BaseRepository
                                [FeedbackSection, FeedbackSectionCreate, FeedbackSectionUpdate,  FeedbackSectionOut]):

    def __init__(self, db: AsyncSession):
        super().__init__(db, FeedbackSection, FeedbackSectionOut)

