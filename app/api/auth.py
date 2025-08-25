from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_async_session
from app.schemas.user import UserCreate, UserAuth, UserOut, Token
from app.schemas.response import SuccessResponse, ErrorResponse
from app.services.user import UserService

router = APIRouter(prefix="/auth", tags=["Auth"])


def get_user_service(db: AsyncSession = Depends(get_async_session)) -> UserService:
    return UserService(db)


@router.post("/register", response_model=SuccessResponse[UserOut], responses={400: {"model": ErrorResponse}})
async def register(user_data: UserCreate, service: UserService = Depends(get_user_service)):
    try:
        user = await service.register(user_data)
        return SuccessResponse(message="Регистрация успешна", data=user)
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ErrorResponse(message=str(e)).dict()
        )


@router.post(
    "/login",
    response_model=SuccessResponse[dict],
    responses={401: {"model": ErrorResponse}}
)
async def login(auth_data: UserAuth, service: UserService = Depends(get_user_service)):
    try:
        user_id, token = await service.authenticate(auth_data)  # теперь возвращаем user_id
        return SuccessResponse(
            message="Авторизация успешна",
            data={
                "user_id": user_id,
                "access_token": token,
                "token_type": "bearer"
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=ErrorResponse(message=str(e)).dict()
        )