from typing import Dict, Any, Optional
import asyncpg
from config.settings import settings

class DatabaseManager:
    def __init__(self):
        self.pool = None

    async def connect(self):
        if not self.pool:
            self.pool = await asyncpg.create_pool(
                settings.DATABASE_URL,
                min_size=5,
                max_size=20
            )

    async def disconnect(self):
        if self.pool:
            await self.pool.close()
            self.pool = None

    async def store_boe_entry(self, entry_id: str, content: str, metadata: Dict[str, Any]) -> bool:
        async with self.pool.acquire() as conn:
            try:
                await conn.execute('''
                    INSERT INTO boe_entries (entry_id, content, metadata)
                    VALUES ($1, $2, $3)
                    ON CONFLICT (entry_id) DO NOTHING
                ''', entry_id, content, metadata)
                return True
            except Exception as e:
                print(f"Error storing BOE entry: {e}")
                return False

    async def store_analysis(self, entry_id: str, summary: str, keywords: list, relevance_score: float) -> Optional[int]:
        async with self.pool.acquire() as conn:
            try:
                return await conn.fetchval('''
                    INSERT INTO analyzed_content (entry_id, summary, keywords, relevance_score)
                    VALUES ($1, $2, $3, $4)
                    RETURNING id
                ''', entry_id, summary, keywords, relevance_score)
            except Exception as e:
                print(f"Error storing analysis: {e}")
                return None

    async def store_report(self, content_id: int, summary: str, recipients: list) -> Optional[int]:
        async with self.pool.acquire() as conn:
            try:
                return await conn.fetchval('''
                    INSERT INTO reports (content_id, summary, recipients)
                    VALUES ($1, $2, $3)
                    RETURNING id
                ''', content_id, summary, recipients)
            except Exception as e:
                print(f"Error storing report: {e}")
                return None 