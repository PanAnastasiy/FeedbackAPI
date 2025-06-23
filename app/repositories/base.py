from typing import Optional, Generic, TypeVar, Type, List

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, inspect
from sqlalchemy.orm import selectinload

# Типы для обобщённого репозитория
ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
OutSchemaType = TypeVar("OutSchemaType", bound=BaseModel)


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType, OutSchemaType]):
    def __init__(
        self,
        db: AsyncSession,
        model: Type[ModelType],
        out_schema: Type[OutSchemaType],
    ):
        self.db = db
        self.model = model
        self.out_schema = out_schema

    async def create(self, obj_in: CreateSchemaType) -> OutSchemaType:
        db_obj = self.model(**obj_in.model_dump())
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return self._to_schema(db_obj)

    async def get_by_id(self, obj_id: int) -> Optional[OutSchemaType]:
        stmt = select(self.model).where(self.model.id == obj_id)
        stmt = self._with_relationships(stmt)

        result = await self.db.execute(stmt)
        obj = result.scalar_one_or_none()
        return self._to_schema(obj) if obj else None

    async def get_all(self) -> List[OutSchemaType]:
        stmt = select(self.model)
        stmt = self._with_relationships(stmt)

        result = await self.db.execute(stmt)
        objs = result.scalars().all()
        return [self._to_schema(obj) for obj in objs]

    async def update(self, obj_id: int, obj_in: UpdateSchemaType) -> Optional[OutSchemaType]:
        result = await self.db.execute(select(self.model).where(self.model.id == obj_id))
        db_obj = result.scalar_one_or_none()
        if not db_obj:
            return None

        for field, value in obj_in.model_dump(exclude_unset=True).items():
            setattr(db_obj, field, value)

        await self.db.commit()
        await self.db.refresh(db_obj)
        return self._to_schema(db_obj)

    async def delete(self, obj_id: int) -> bool:
        result = await self.db.execute(select(self.model).where(self.model.id == obj_id))
        db_obj = result.scalar_one_or_none()
        if not db_obj:
            return False

        await self.db.delete(db_obj)
        await self.db.commit()
        return True

    def _with_relationships(self, stmt):
        mapper = inspect(self.model)
        for relation in mapper.relationships.keys():
            stmt = stmt.options(selectinload(getattr(self.model, relation)))
        return stmt

    def _to_schema(self, obj: ModelType) -> OutSchemaType:
        return self.out_schema.model_validate(obj, from_attributes=True)

    async def create_raw(self, data: dict) -> ModelType:
        db_obj = self.model(**data)
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def update_raw(self, obj_id: int, data: dict) -> Optional[ModelType]:
        result = await self.db.execute(select(self.model).where(self.model.id == obj_id))
        db_obj = result.scalar_one_or_none()

        if not db_obj:
            return None

        for field, value in data.items():
            setattr(db_obj, field, value)

        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj
