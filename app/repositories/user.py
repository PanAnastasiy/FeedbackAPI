from typing import Optional
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.repositories.base import BaseRepository
from app.schemas.user import UserCreate, UserUpdate, UserOut


class UserRepository(BaseRepository[
    User, UserCreate, UserUpdate, UserOut
]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db, User, UserOut)

    async def get_by_email_or_username(self, email: str, username: str) -> Optional[User]:
        stmt = select(self.model).where(
            or_(self.model.email == email, self.model.username == username)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
