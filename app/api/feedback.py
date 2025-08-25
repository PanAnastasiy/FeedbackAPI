# api/feedback.py

from fastapi import APIRouter, Depends, HTTPException

from app.services.feedback import FeedbackService
from app.schemas.feedback import FeedbackCreate, FeedbackUpdate
from app.utils.get_current_user import get_current_user
from app.utils.get_service import get_service


router = APIRouter(prefix="/feedbacks", tags=["Feedback"])


@router.post("/")
async def create_feedback(
    feedback_in: FeedbackCreate,
    service: FeedbackService = Depends(get_service(FeedbackService)),
current_user=Depends(get_current_user)
):
    return await service.create(feedback_in)


@router.get("/")
async def get_all_feedbacks(service: FeedbackService = Depends(get_service(FeedbackService)), current_user=Depends(get_current_user)):
    return await service.get_all()


@router.get("/{feedback_id}")
async def get_feedback(
    feedback_id: int,
    service: FeedbackService = Depends(get_service(FeedbackService)),
    current_user=Depends(get_current_user)
):
    feedback = await service.get_by_id(feedback_id)
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return feedback


@router.put("/{feedback_id}")
async def update_feedback(
    feedback_id: int,
    feedback_in: FeedbackUpdate,
    service: FeedbackService = Depends(get_service(FeedbackService)),
):
    return await service.update(feedback_id, feedback_in)


@router.delete("/{feedback_id}")
async def delete_feedback(
    feedback_id: int,
    service: FeedbackService = Depends(get_service(FeedbackService)),
    current_user=Depends(get_current_user)
):
    return await service.delete(feedback_id)