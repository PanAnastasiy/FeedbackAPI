from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("TOGETHER_API_KEY"),
    base_url="https://api.together.xyz/v1",  # это важно!
)


async def generate_feedback(keywords: list[str]) -> str:
    prompt = (
        "Составь профессиональный на, грамотный и краткий фидбек по кандидату НА РУССКОМ ЯЗЫКЕ, основываясь на следующих ключевых фразах:\n\n"
        + "\n".join(f"- {kw}" for kw in keywords) + "НА РУССКОМ ЯЗЫКЕ !!!"
    )

    response = client.chat.completions.create(
        model="mistralai/Mixtral-8x7B-Instruct-v0.1",  # или другая модель с https://docs.together.ai/docs/inference-models
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,
        temperature=0.7
    )

    return response.choices[0].message.content.strip()
