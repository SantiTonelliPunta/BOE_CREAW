from typing import Optional
from models.schemas import BOEEntry, AnalyzedContent, Report
from utils.monitoring import SimpleMonitor
from utils.cache import SimpleCache

class BOEWorkflow:
    def __init__(self, agents, monitor: SimpleMonitor, cache: SimpleCache):
        self.agents = agents
        self.monitor = monitor
        self.cache = cache

    async def process_entry(self, entry_id: str) -> Optional[Report]:
        try:
            # 1. Monitorización y extracción
            boe_entry = await self.agents.monitor_agent.execute_task(
                "extract_boe_content",
                {"entry_id": entry_id}
            )
            await self.monitor.log_performance("extraction", {"entry_id": entry_id})

            # 2. Análisis de contenido
            analyzed_content = await self.agents.analysis_agent.execute_task(
                "analyze_content",
                {"boe_entry": boe_entry}
            )
            
            # 3. Persistencia
            stored_data = await self.agents.database_agent.execute_task(
                "store_content",
                {"analyzed_content": analyzed_content}
            )

            # 4. Generación de reporte
            report = await self.agents.report_agent.execute_task(
                "generate_report",
                {"stored_data": stored_data}
            )

            # 5. Control de calidad
            is_valid = await self.agents.quality_agent.execute_task(
                "validate_report",
                {"report": report}
            )

            if not is_valid:
                raise ValueError("Report failed quality validation")

            # 6. Notificación
            if is_valid:
                await self.agents.notification_agent.execute_task(
                    "send_report",
                    {"report": report}
                )

            return report

        except Exception as e:
            await self.monitor.log_performance(
                "error",
                {
                    "entry_id": entry_id,
                    "error": str(e),
                    "stage": "process_entry"
                }
            )
            raise 