from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.base import BaseRepository
from app.schemas.user import UserCreate, UserUpdate, UserOut


class UserRepository(BaseRepository[
    User, UserCreate, UserUpdate, UserOut
]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db, User, UserOut)
