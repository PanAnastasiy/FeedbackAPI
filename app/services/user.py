from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.repositories.role import RoleRepository
from app.repositories.user import UserRepository
from app.schemas.user import UserUpdate, UserCreate
from app.services.base import BaseService
from app.utils.hash_password import hash_password


class UserService(BaseService[User, UserCreate, UserUpdate]):
    def __init__(self, db: AsyncSession):
        super().__init__(UserRepository(db))
        self.role_repo = RoleRepository(db)

    async def create(self, obj_in: UserCreate) -> User:
        data = obj_in.model_dump(exclude_unset=True)

        # Хешируем пароль
        raw_password = data.pop("password")
        data["hashed_password"] = hash_password(raw_password)

        # По имени роли ищем ID
        role_name = data.pop("role", None)
        if role_name:
            role = await self.role_repo.get_by_name(role_name)
            if not role:
                raise ValueError(f"Роль '{role_name}' не найдена")
            data["role_id"] = role.id

        user = self.repository.model(**data)
        self.repository.db.add(user)
        await self.repository.db.commit()
        await self.repository.db.refresh(user)
        return user

    async def update(self, obj_id: int, obj_in: UserUpdate) -> Optional[User]:
        data = obj_in.model_dump(exclude_unset=True)
        status_name = data.pop("status", None)

        if status_name is not None:
            status_obj = await self.role_repo.get_by_name(status_name)
            if not status_obj:
                raise ValueError(f"Статус '{status_name}' не найден.")
            data["status_id"] = status_obj.id

        return await self.repository.update_raw(obj_id, data)