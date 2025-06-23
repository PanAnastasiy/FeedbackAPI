from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.base import BaseRepository


class SkillRepository(BaseRepository):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db, Skill)
