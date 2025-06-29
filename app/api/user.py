from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_async_session
from app.utils.get_service import get_service
from app.schemas.user import UserCreate, UserUpdate
from app.services.user import UserService

router = APIRouter()


@router.get("/users")
async def get_users(session: AsyncSession = Depends(get_async_session)):
    try:
        service = UserService(session)
        return await service.get_all()
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Ошибка при получении пользователей: {str(e)}")


@router.post("/users")
async def create_user(
    user_in: UserCreate,
    service: UserService = Depends(get_service(UserService)),
):
    return await service.create(user_in)


@router.get("/users/{user_id}")
async def get_user(
    user_id: int,
    service: UserService = Depends(get_service(UserService)),
):
    return await service.get_by_id(user_id)


@router.put("/users/{user_id}")
async def update_user(
    user_id: int,
    user_in: UserUpdate,
    service: UserService = Depends(get_service(UserService)),
):
    return await service.update(user_id, user_in)


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    service: UserService = Depends(get_service(UserService)),
):
    return await service.delete(user_id)
