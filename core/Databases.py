import asyncpg
from typing import Optional

class Database:
    def __init__(self):
        self.pool: Optional[asyncpg.Pool] = None

    async def connect(self, dsn: str):
        self.pool = await asyncpg.create_pool(dsn=dsn, min_size=2, max_size=10)

    async def disconnect(self):
        if self.pool:
            await self.pool.close()

    async def fetch_one(self, query: str, *args):
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(query, *args)

    async def fetch_all(self, query: str, *args):
        async with self.pool.acquire() as conn:
            return await conn.fetch(query, *args)

    async def execute(self, query: str, *args):
        async with self.pool.acquire() as conn:
            return await conn.execute(query, *args)


db = Database()
