from fastapi import APIRouter, HTTPException

from app.schemas.feedback import FeedbackRequest
from app.services.feedback_generator import generate_feedback
from fastapi import Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/feedback", tags=["feedback"])
templates = Jinja2Templates(directory="templates")


@router.post("/generate")
async def generate_feedback_endpoint(request: FeedbackRequest):
    try:
        feedback = await generate_feedback(request.keywords)
        return {"feedback": feedback}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/form", response_class=HTMLResponse)
async def feedback_form(request: Request):
    return templates.TemplateResponse("feedback_form.html", {"request": request})


@router.post("/generate_html", response_class=HTMLResponse)
async def generate_feedback_form(request: Request, keywords: str = Form(...)):
    try:
        feedback = await generate_feedback(keywords)
        return templates.TemplateResponse("feedback_form.html", {
            "request": request,
            "feedback": feedback
        })
    except Exception as e:
        return templates.TemplateResponse("feedback_form.html", {
            "request": request,
            "error": str(e)
        })
