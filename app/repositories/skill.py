from sqlalchemy.ext.asyncio import AsyncSession

from app.models.skill import Skill
from app.repositories.base import BaseRepository
from app.schemas.skill import SkillOut, SkillCreate, SkillUpdate


class SkillRepository(BaseRepository[
    Skill, SkillCreate, SkillUpdate, SkillOut
]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db, Skill, SkillOut)
