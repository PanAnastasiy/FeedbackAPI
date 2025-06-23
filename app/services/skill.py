from sqlalchemy.ext.asyncio import AsyncSession

from app.models.skill import Skill
from app.repositories.skill import SkillRepository
from app.schemas.skill import SkillCreate, SkillUpdate
from app.services.base import BaseService


class SkillService(BaseService[Skill, SkillCreate, SkillUpdate]):
    def __init__(self, db: AsyncSession):
        super().__init__(SkillRepository(db))
