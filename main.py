import asyncio
from agents.core_agents import BOEAgents
from core.workflow import BOEWorkflow
from utils.monitoring import SimpleMonitor
from utils.cache import SimpleCache

async def main():
    # Inicializar componentes
    agents = BOEAgents()
    monitor = SimpleMonitor()
    cache = SimpleCache()
    
    # Crear workflow
    workflow = BOEWorkflow(agents, monitor, cache)
    
    # Procesar una entrada de ejemplo
    try:
        report = await workflow.process_entry("example_entry_id")
        print(f"Processed report: {report}")
    except Exception as e:
        print(f"Error processing entry: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 