from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate, UserOut, UserAuth
from app.services.base import BaseService
from app.utils.security import hash_password, verify_password, create_access_token


class UserService(BaseService[User, UserCreate, UserUpdate]):
    def __init__(self, db: AsyncSession):
        repository = UserRepository(db)
        super().__init__(repository)
        self.repository: UserRepository = repository

    async def register(self, user_data: UserCreate):
        # Проверка уникальности
        existing_user = await self.repository.get_by_email_or_username(user_data.email, user_data.username)
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email или username уже заняты")

        # Хэшируем пароль
        hashed_password = hash_password(user_data.password)

        # Формируем данные для модели User
        user_dict = user_data.model_dump()
        user_dict.pop("password")  # убираем поле password
        user_dict["hashed_password"] = hashed_password
        user_dict["role_id"] = 1  # например, роль по умолчанию

        # Создаём пользователя
        new_user = await self.repository.create_raw(user_dict)
        return new_user

    async def authenticate(self, auth_data: UserAuth) -> str:
        """
        Аутентификация пользователя по email и паролю.
        Возвращает JWT токен при успешной проверке.
        """
        user = await self.repository.get_by_email_or_username(auth_data.email, auth_data.email)
        if not user or not verify_password(auth_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный email или пароль"
            )

        return create_access_token({"sub": str(user.id)})
