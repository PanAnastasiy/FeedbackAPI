from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_async_session
from app.services.candidate_status import CandidateStatusService
from app.schemas.candidate_status import CandidateStatusCreate, CandidateStatusUpdate
from app.utils.get_service import get_service

router = APIRouter()


@router.get("/statuses")
async def get_statuses(session: AsyncSession = Depends(get_async_session)):
    try:
        service = CandidateStatusService(session)
        return await service.get_all()
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Ошибка при получении: {str(e)}")


@router.post("/statuses")
async def create_status(
    status_in: CandidateStatusCreate,
    service: CandidateStatusService = Depends(get_service(CandidateStatusService)),
):
    return await service.create(status_in)


@router.get("/statuses/{status_id}")
async def get_status(
    status_id: int,
    service: CandidateStatusService = Depends(get_service(CandidateStatusService)),
):
    return await service.get_by_id(status_id)


@router.put("/statuses/{status_id}")
async def update_status(
    status_id: int,
    status_in: CandidateStatusUpdate,
    service: CandidateStatusService = Depends(get_service(CandidateStatusService)),
):
    return await service.update(status_id, status_in)


@router.delete("/statuses/{status_id}")
async def delete_status(
    status_id: int,
    service: CandidateStatusService = Depends(get_service(CandidateStatusService)),
):
    return await service.delete(status_id)
