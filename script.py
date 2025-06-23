import asyncio
from sqlalchemy import select
from app.db.database import async_session_maker
from app.models.candidate_status import CandidateStatus


async def test():
    async with async_session_maker() as session:
        result = await session.execute(select(CandidateStatus))
        print(result.scalars().all())

asyncio.run(test())
