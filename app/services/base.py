from typing import Generic, List, Optional, TypeVar

from app.repositories.base import BaseRepository

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")


class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, repository: BaseRepository[ModelType, CreateSchemaType, UpdateSchemaType, any]):
        self.repository = repository

    async def create(self, obj_in: CreateSchemaType) -> ModelType:
        return await self.repository.create(obj_in)

    async def get_all(self) -> List[ModelType]:
        return await self.repository.get_all()

    async def get_by_id(self, obj_id: int) -> Optional[ModelType]:
        return await self.repository.get_by_id(obj_id)

    async def update(self, obj_id: int, obj_in: UpdateSchemaType) -> Optional[ModelType]:
        return await self.repository.update(obj_id, obj_in)

    async def delete(self, obj_id: int) -> bool:
        return await self.repository.delete(obj_id)
