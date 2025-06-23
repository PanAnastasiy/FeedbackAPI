from fastapi import FastAPI

from fastapi import FastAPI
from app.api.feedback import router as feedback_router
from app.api.candidate_status import router as status_router
from app.api.candidate import router as candidate_router
from app.api.skill import router as skill_router
from app.api.habr import router as habr_router

app = FastAPI()

app.include_router(feedback_router)
app.include_router(status_router)
app.include_router(candidate_router)

app.include_router(skill_router)

app.include_router(habr_router)

@app.get("/")
async def root():
    return {"message": "Feedback API is running"}
