from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("TOGETHER_API_KEY"),
    base_url="https://api.together.xyz/v1",  # это важно!
)


async def generate_feedback(keywords: str, section_name: str = "") -> str:
    # Преобразуем строку ключевых слов в список
    keyword_list = [kw.strip() for kw in keywords.split(',') if kw.strip()]

    # Без ключевых слов — вернём сообщение по умолчанию
    if not keyword_list:
        return f"Раздел «{section_name}»: Недостаточно данных для генерации фидбека."

    prompt = (
        f"Составь краткий, профессиональный фидбек на русском языке по кандидату в разделе «{section_name}», "
        "основываясь на следующих ключевых фразах:\n\n" +
        "\n".join(f"- {kw}" for kw in keyword_list) +
        "\n\nОтвет должен быть на русском языке!"
    )

    response = client.chat.completions.create(
        model="mistralai/Mixtral-8x7B-Instruct-v0.1",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,
        temperature=0.7
    )

    return response.choices[0].message.content.strip()

