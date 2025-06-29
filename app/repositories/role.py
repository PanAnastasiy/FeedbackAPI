from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.role import Role
from app.repositories.base import BaseRepository
from app.schemas.role import RoleCreate, RoleUpdate, RoleOut


class RoleRepository(BaseRepository[
    Role, RoleCreate, RoleUpdate, RoleOut
]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db, Role, RoleOut)

    async def get_by_name(self, name: str) -> Role | None:
        stmt = select(Role).where(Role.name == name)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
