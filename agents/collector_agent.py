from datetime import datetime
import aiohttp
import feedparser
from typing import List, Dict
from crew import Agent
import json

class BOECollectorAgent(Agent):
    def __init__(self):
        self.name = "BOE RSS Collector"
        self.goal = "Recolectar y procesar entradas RSS del BOE"
        self.backstory = "Especializado en monitorear y extraer información del feed RSS del BOE"
        self.rss_url = "https://www.boe.es/rss/boe.php?s=3"

    async def parse_boe_entry(self, entry) -> Dict:
        """Procesa una entrada individual del BOE"""
        # Extrae el ID del BOE de la URL
        boe_id = entry.get('id', '').split('=')[-1] if entry.get('id') else None
        
        # Estructura los metadatos
        metadata = {
            'title': entry.get('title', ''),
            'department': entry.get('category', ''),  # Departamento/Ministerio
            'publication_date': entry.get('published', ''),
            'link': entry.get('link', ''),
            'section': self._extract_section(entry.get('title', '')),
            'document_type': self._extract_document_type(entry.get('title', '')),
        }

        return {
            'id': boe_id,
            'content': entry.get('summary', ''),
            'metadata': metadata,
            'processed_at': datetime.now().isoformat()
        }

    def _extract_section(self, title: str) -> str:
        """Extrae la sección del título"""
        sections = {
            'I': 'Disposiciones Generales',
            'II': 'Autoridades y Personal',
            'III': 'Otras Disposiciones',
            'IV': 'Administración de Justicia',
            'V': 'Anuncios'
        }
        for section, name in sections.items():
            if section in title:
                return name
        return 'Otros'

    def _extract_document_type(self, title: str) -> str:
        """Extrae el tipo de documento del título"""
        types = ['Real Decreto', 'Orden', 'Resolución', 'Acuerdo', 'Convenio']
        for doc_type in types:
            if doc_type in title:
                return doc_type
        return 'Otros'

    async def fetch_rss_feed(self) -> List[Dict]:
        """Obtiene las entradas del RSS del BOE"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.rss_url) as response:
                    if response.status == 200:
                        content = await response.text()
                        feed = feedparser.parse(content)
                        
                        entries = []
                        for entry in feed.entries:
                            parsed_entry = await self.parse_boe_entry(entry)
                            entries.append(parsed_entry)
                        
                        self.log.info(f"Recolectadas {len(entries)} entradas del BOE")
                        return entries
                    else:
                        raise Exception(f"Error fetching RSS: {response.status}")
        except Exception as e:
            self.log.error(f"Error en la recolección RSS: {str(e)}")
            return []

    async def store_entries(self, entries: List[Dict]) -> bool:
        """Almacena las entradas en la base de datos"""
        try:
            async with self.db.session() as session:
                for entry in entries:
                    query = """
                    INSERT INTO boe_entries (id, content, metadata, processed_at)
                    VALUES (:id, :content, :metadata::jsonb, :processed_at)
                    ON CONFLICT (id) DO UPDATE 
                    SET content = EXCLUDED.content,
                        metadata = EXCLUDED.metadata::jsonb,
                        processed_at = EXCLUDED.processed_at
                    """
                    await session.execute(query, {
                        'id': entry['id'],
                        'content': entry['content'],
                        'metadata': json.dumps(entry['metadata']),
                        'processed_at': entry['processed_at']
                    })
                await session.commit()
            return True
        except Exception as e:
            self.log.error(f"Error al almacenar entradas: {str(e)}")
            return False

    async def run(self):
        """Método principal que ejecuta el ciclo de recolección"""
        self.log.info("Iniciando recolección de RSS del BOE")
        entries = await self.fetch_rss_feed()
        
        if entries:
            self.log.info(f"Encontradas {len(entries)} nuevas entradas")
            if await self.store_entries(entries):
                self.log.info("Entradas almacenadas correctamente")
                return True
        return False 