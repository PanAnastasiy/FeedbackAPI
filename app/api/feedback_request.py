from fastapi import APIRouter, HTTPException

from app.schemas.generate_request import GenerateRequest
from app.services.feedback_generator import generate_feedback
from fastapi import Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.post("/generate")
async def generate_feedback_endpoint(request: GenerateRequest):
    try:
        # Здесь можно использовать section_name при генерации
        feedback = await generate_feedback(request.keywords, section_name=request.section_name)
        return {"generated_text": feedback}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
