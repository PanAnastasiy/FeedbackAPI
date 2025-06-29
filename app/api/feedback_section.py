from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


from app.db.database import get_async_session
from app.schemas.feedback_section import FeedbackSectionCreate, FeedbackSectionUpdate
from app.services.feedback_sections import FeedbackSectionService
from app.utils.get_service import get_service

router = APIRouter()


@router.get("/sections")
async def get_sections(session: AsyncSession = Depends(get_async_session)):
    try:
        service = FeedbackSectionService(session)
        return await service.get_all()
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Ошибка при получении секций: {str(e)}")


@router.post("/sections")
async def create_section(
    section_in: FeedbackSectionCreate,
    service: FeedbackSectionService = Depends(get_service(FeedbackSectionService)),
):
    return await service.create(section_in)


@router.get("/sections/{section_id}")
async def get_section(
    section_id: int,
    service: FeedbackSectionService = Depends(get_service(FeedbackSectionService)),
):
    return await service.get_by_id(section_id)


@router.put("/sections/{section_id}")
async def update_section(
    section_id: int,
    section_in: FeedbackSectionUpdate,
    service: FeedbackSectionService = Depends(get_service(FeedbackSectionService)),
):
    return await service.update(section_id, section_in)


@router.delete("/sections/{section_id}")
async def delete_section(
    section_id: int,
    service: FeedbackSectionService = Depends(get_service(FeedbackSectionService)),
):
    return await service.delete(section_id)
