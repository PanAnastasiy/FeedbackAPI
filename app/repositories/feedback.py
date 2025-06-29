from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import FeedbackItem
from app.models.feedback import Feedback
from app.repositories.base import BaseRepository
from app.schemas.feedback import FeedbackUpdate, FeedbackCreate, FeedbackOut


class FeedbackRepository(BaseRepository[
    Feedback, FeedbackCreate, FeedbackUpdate, FeedbackOut
]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db, Feedback, FeedbackOut)

    async def create_raw(self, data: dict):
        # 1. Извлечь и удалить из словаря поле 'items'
        items_data = data.pop("items", [])

        # 2. Создать основной объект Feedback без items
        db_obj = self.model(**data)

        # 3. Создать ORM-экземпляры FeedbackItem
        db_obj.items = [FeedbackItem(**item) for item in items_data]

        # 4. Сохранить в базу
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)

        return db_obj

    async def update_raw(self, obj_id: int, data: dict):
        items_data = data.pop("items", None)  # Забираем items

        # Загружаем объект с items
        result = await self.db.execute(
            select(self.model)
            .options(selectinload(self.model.items))
            .where(self.model.id == obj_id)
        )
        db_obj = result.scalar_one_or_none()
        if not db_obj:
            return None

        # Обновляем простые поля
        for field, value in data.items():
            setattr(db_obj, field, value)

        if items_data is not None:
            # Проверяем, что у всех items есть section_id
            for item in items_data:
                if "section_id" not in item or item["section_id"] is None:
                    raise ValueError(f"section_id is required for each feedback item: {item}")

            # Удаляем старые items
            await self.db.execute(
                delete(FeedbackItem).where(FeedbackItem.feedback_id == obj_id)
            )
            await self.db.flush()  # Применяем удаление

            # Очищаем текущие связанные items
            db_obj.items.clear()

            # Добавляем новые items по одному
            for item in items_data:
                new_item = FeedbackItem(feedback_id=obj_id, **item)
                db_obj.items.append(new_item)

        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj
