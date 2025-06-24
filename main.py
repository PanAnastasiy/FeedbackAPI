from fastapi import FastAPI
from app.api.feedback import router as feedback_router
from app.api.candidate_status import router as status_router
from app.api.candidate import router as candidate_router
from app.api.skill import router as skill_router
from app.api.habr import router as habr_router
from app.api.feedback_section import router as section_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(feedback_router)
app.include_router(status_router)
app.include_router(candidate_router)

app.include_router(skill_router)

app.include_router(habr_router)

app.include_router(section_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Feedback API is running"}
