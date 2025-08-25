from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, TIMESTAMP, ForeignKey, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship

from app.db.base import Base
from sqlalchemy.orm import Session
from app.db.database import get_async_session
from fastapi import Depends


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)
    role_obj = relationship('Role')

    @classmethod
    async def get_by_id(cls, user_id: int, db: AsyncSession):
        result = await db.execute(select(cls).where(cls.id == user_id))
        return result.scalars().first()

