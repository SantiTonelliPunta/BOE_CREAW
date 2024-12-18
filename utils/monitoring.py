from datetime import datetime
from typing import Dict, Any

class SimpleMonitor:
    async def log_performance(self, operation: str, data: Dict[str, Any]):
        timestamp = datetime.now()
        # Logging básico de operaciones críticas
        print(f"[{timestamp}] {operation}: {data}") 