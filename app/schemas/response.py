from pydantic import BaseModel
from typing import Generic, Optional, TypeVar

T = TypeVar("T")


class BaseResponse(BaseModel, Generic[T]):
    success: bool
    message: str
    data: Optional[T] = None


class SuccessResponse(BaseResponse[T]):
    success: bool = True


class ErrorResponse(BaseResponse[None]):
    success: bool = False
    data: None = None
