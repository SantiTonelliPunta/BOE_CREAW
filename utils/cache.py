from functools import lru_cache
from typing import Any

class SimpleCache:
    @lru_cache(maxsize=100)
    async def get_boe_content(self, url: str) -> Any:
        # Implementación básica de cache para contenido frecuente
        pass 