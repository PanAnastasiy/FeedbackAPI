from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import OperationalError
from asyncpg.exceptions import ConnectionDoesNotExistError
import asyncio

DATABASE_URL = "postgresql+asyncpg://postgres:hLixrCFMIypVYjduqpgkCiggoVqPchxK@yamanote.proxy.rlwy.net:44867/railway"

engine = create_async_engine(
    DATABASE_URL,
    echo=True,              # Логирование запросов
    pool_pre_ping=True,     # Проверка соединений перед использованием
    pool_recycle=1800,      # Пересоздавать соединения каждые 30 минут
    pool_size=10,           # Размер пула соединений
    max_overflow=5,         # Дополнительные соединения при нагрузке
    pool_timeout=30,        # Таймаут ожидания соединения (сек)
)

async_session_maker = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_async_session():
    max_retries = 3  # Максимальное количество попыток
    retry_delay = 1  # Начальная задержка между попытками

    for attempt in range(max_retries):
        try:
            async with async_session_maker() as session:
                yield session
            break
        except (OperationalError, ConnectionDoesNotExistError) as e:
            if attempt == max_retries - 1:  # Если это последняя попытка
                raise
            await asyncio.sleep(retry_delay * (attempt + 1))  # Увеличиваем задержку
