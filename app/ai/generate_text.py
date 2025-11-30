from data.redis.redis_manager import redis_manager
from openai import AsyncOpenAI
from config import VENICE
import bleach
import re

client = AsyncOpenAI(
    api_key=VENICE,
    base_url="https://api.venice.ai/api/v1"
)

prices: dict[str, int] = {
    "openai-gpt-oss-120b": 2,
    "google-gemma-3-27b-it": 2,
    "qwen3-4b": 1,
    "venice-uncensored": 6,
    "mistral-31-24b": 13,
    "qwen3-235b": 23,
    "zai-org-glm-4.6": 18,
    "llama-3.3-70b": 19
}

async def generate_ai_response(tg_id: int, model: str, query: str):
    try:
        history = await redis_manager.get_history(tg_id)
        print("История (словари):", history)
        
        messages = [
            {"role": "system", "content": "Если надо оформить текст используй только эти тэги HTML: <b>, <i>, <code>, <pre>"},
            *(history if history else []),
            {"role": "user", "content": query}
        ]
        print(messages)

        completion = await client.chat.completions.create(
            model=model,
            max_tokens=900,
            frequency_penalty=0.5,
            stream=False,
            messages=messages
            )

        text = completion.choices[0].message.content
        text = str(re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL))

        text = bleach.clean(
            text=text,
            tags=['b', 'i', 'code', 'pre'],
            attributes={},
            strip=True,
            strip_comments=True
        )
        print(text)

        await redis_manager.add_history(tg_id=tg_id, role="user", content=query)
        await redis_manager.add_history(tg_id=tg_id, role="assistant", content=text)

        return text
    except Exception as e:
        print(e)
        return "Произошла ошибка"