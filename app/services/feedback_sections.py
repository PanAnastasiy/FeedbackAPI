from sqlalchemy.ext.asyncio import AsyncSession

from app.models.feedback_section import FeedbackSection
from app.repositories.feedback_section import FeedbackSectionRepository
from app.schemas.feedback_sections import FeedbackSectionCreate, FeedbackSectionUpdate
from app.services.base import BaseService


class FeedbackSectionService(BaseService[FeedbackSection, FeedbackSectionCreate, FeedbackSectionUpdate]):

    def __init__(self, db: AsyncSession):
        super().__init__(FeedbackSectionRepository(db))
