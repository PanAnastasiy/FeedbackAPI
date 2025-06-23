from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Type, TypeVar, Callable

from app.db.database import get_async_session

T = TypeVar("T")


def get_service(service_class: Type[T]) -> Callable[[AsyncSession], T]:
    def _get_service(session: AsyncSession = Depends(get_async_session)) -> T:
        return service_class(session)
    return _get_service
