from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.skill import SkillCreate, SkillUpdate
from app.services.skill import SkillService
from app.db.database import get_async_session
from app.utils.get_current_user import get_current_user
from app.utils.get_service import get_service

router = APIRouter()


@router.get("/skills")
async def get_skills(session: AsyncSession = Depends(get_async_session), current_user=Depends(get_current_user)):
    try:
        service = SkillService(session)
        return await service.get_all()
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Ошибка при получении навыков: {str(e)}")


@router.post("/skills")
async def create_skill(
    skill_in: SkillCreate,
    service: SkillService = Depends(get_service(SkillService)), current_user=Depends(get_current_user)
):
    return await service.create(skill_in)


@router.get("/skills/{skill_id}")
async def get_skill(
    skill_id: int,
    service: SkillService = Depends(get_service(SkillService)), current_user=Depends(get_current_user)
):
    return await service.get_by_id(skill_id)


@router.put("/skills/{skill_id}")
async def update_skill(
    skill_id: int,
    skill_in: SkillUpdate,
    service: SkillService = Depends(get_service(SkillService)), current_user=Depends(get_current_user)
):
    return await service.update(skill_id, skill_in)


@router.delete("/skills/{skill_id}")
async def delete_skill(
    skill_id: int,
    service: SkillService = Depends(get_service(SkillService)), current_user=Depends(get_current_user)
):
    return await service.delete(skill_id)
