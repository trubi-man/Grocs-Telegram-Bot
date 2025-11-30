import redis.asyncio as redis
import json

class AsyncRedisManager():
    def __init__(self):
        self.r = redis.Redis(decode_responses=True)

    async def add_history(self, tg_id: int, role: str, content: str):
        message = json.dumps({"role": role, "content": content}, ensure_ascii=False)
        await self.r.lpush(f"chat:{tg_id}", message)
        await self.r.ltrim(f"chat:{tg_id}", 0, 3)

    async def get_history(self, tg_id: int) -> list:
        history_json = await self.r.lrange(f"chat:{tg_id}", 0, -1)
        history_dicts = []

        for item in history_json:
            history_dicts.append(json.loads(item))

        return history_dicts
    
    async def clear_history(self, tg_id: int):
        await self.r.delete(f"chat:{tg_id}")

    async def set_query(self, tg_id: int | str, query: str):
        await self.r.set(name=str(tg_id), value=query, ex=500)

    async def get_query(self, tg_id: int | str) -> str | None:
        query = await self.r.get(str(tg_id))
        return query

redis_manager = AsyncRedisManager()