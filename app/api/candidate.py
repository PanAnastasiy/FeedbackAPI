from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.database import get_async_session
from app.services.candidate import CandidateService
from app.schemas.candidate import CandidateCreate, CandidateUpdate, CandidateOut
from app.utils.get_current_user import get_current_user
from app.utils.get_service import get_service

router = APIRouter()


@router.get("/candidates", response_model=List[CandidateOut])
async def get_candidates(session: AsyncSession = Depends(get_async_session), current_user=Depends(get_current_user)):
    try:
        service = CandidateService(session)
        return await service.get_all()
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Ошибка при получении: {str(e)}")


@router.post("/candidates")
async def create_candidate(
    candidate_in: CandidateCreate,
    service: CandidateService = Depends(get_service(CandidateService)),
    current_user=Depends(get_current_user)
):
    return await service.create(candidate_in)


@router.get("/candidates/{candidate_id}")
async def get_candidate(
    candidate_id: int,
    service: CandidateService = Depends(get_service(CandidateService)),
    current_user=Depends(get_current_user)
):
    return await service.get_by_id(candidate_id)


@router.put("/candidates/{candidate_id}")
async def update_candidate(
    candidate_id: int,
    candidate_in: CandidateUpdate,
    service: CandidateService = Depends(get_service(CandidateService)),
    current_user=Depends(get_current_user)
):
    return await service.update(candidate_id, candidate_in)


@router.delete("/candidates/{candidate_id}")
async def delete_candidate(
    candidate_id: int,
    service: CandidateService = Depends(get_service(CandidateService)),
    current_user=Depends(get_current_user)
):
    return await service.delete(candidate_id)
