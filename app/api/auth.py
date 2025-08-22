from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_async_session
from app.schemas.user import UserCreate, UserAuth, UserOut, Token
from app.services.user import UserService

router = APIRouter(prefix="/auth", tags=["Auth"])


# Зависимость для создания UserService
def get_user_service(db: AsyncSession = Depends(get_async_session)) -> UserService:
    return UserService(db)


@router.post("/register", response_model=UserOut)
async def register(
    user_data: UserCreate,
    service: UserService = Depends(get_user_service)
):
    """
    Регистрация нового пользователя.
    """
    return await service.register(user_data)


@router.post("/login", response_model=Token)
async def login(
    auth_data: UserAuth,
    service: UserService = Depends(get_user_service)
):
    """
    Авторизация пользователя. Возвращает JWT токен.
    """
    token = await service.authenticate(auth_data)
    return {"access_token": token, "token_type": "bearer"}
