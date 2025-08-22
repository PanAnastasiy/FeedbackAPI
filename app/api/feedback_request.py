from fastapi import APIRouter, HTTPException

from app.schemas.generate_request import GenerateRequest
from app.services.feedback_generator import generate_feedback, client
from fastapi import Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.post("/generate")
async def generate(req: GenerateRequest):
    keyword_list = [kw.strip() for kw in req.keywords.split(',') if kw.strip()]
    skill_lines = [f"{skill.name} (уровень {skill.level}/5)" for skill in req.skills]
    all_clues = keyword_list + skill_lines

    if not all_clues:
        return {"generated_text": f"Раздел «{req.section_name}»: Недостаточно данных для генерации фидбека."}

    prompt = (
        f"Составь краткий, профессиональный фидбек на русском языке по кандидату в разделе «{req.section_name}», "
        "на основе следующих ключевых пунктов:\n\n" +
        "\n".join(f"- {line}" for line in all_clues) +
        "\n\nОтвет должен быть на русском языке!"
    )

    response = client.chat.completions.create(
        model="mistralai/Mixtral-8x7B-Instruct-v0.1",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0.7,
    )

    return {"generated_text": response.choices[0].message.content.strip()}
