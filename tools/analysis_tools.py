from openai import AsyncOpenAI
from config.settings import settings
from typing import Dict, Any
from crewai import Tool

class AnalysisTools:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    @staticmethod
    def gpt_analyzer() -> Tool:
        async def analyze_content(content: str) -> Dict[str, Any]:
            try:
                client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
                response = await client.chat.completions.create(
                    model=settings.GPT_MODEL,
                    messages=[
                        {"role": "system", "content": "Eres un experto en análisis de documentos legales del BOE. Tu tarea es analizar el contenido y extraer los puntos más relevantes."},
                        {"role": "user", "content": f"Analiza el siguiente contenido del BOE y extrae los puntos clave:\n\n{content}"}
                    ],
                    max_tokens=settings.GPT_MAX_TOKENS,
                    temperature=0.3
                )
                
                return {
                    "summary": response.choices[0].message.content,
                    "keywords": extract_keywords(response.choices[0].message.content),
                    "relevance_score": calculate_relevance(response.choices[0].message.content)
                }
            except Exception as e:
                raise Exception(f"Error al analizar contenido con GPT: {str(e)}")

        return Tool(
            name="GPT Analyzer",
            description="Analiza contenido del BOE usando GPT-3.5",
            func=analyze_content
        )

    @staticmethod
    def categorizer() -> Tool:
        async def categorize_content(content: str) -> Dict[str, Any]:
            try:
                client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
                response = await client.chat.completions.create(
                    model=settings.GPT_MODEL,
                    messages=[
                        {"role": "system", "content": "Categoriza este documento del BOE en una o más categorías principales."},
                        {"role": "user", "content": f"Categoriza el siguiente contenido:\n\n{content}"}
                    ],
                    max_tokens=1024,
                    temperature=0.2
                )
                
                return {
                    "categories": response.choices[0].message.content.split(","),
                    "confidence": 0.95
                }
            except Exception as e:
                raise Exception(f"Error al categorizar contenido: {str(e)}")

        return Tool(
            name="Content Categorizer",
            description="Categoriza documentos del BOE",
            func=categorize_content
        )

    @staticmethod
    def relevance_scorer() -> Tool:
        async def score_relevance(content: str, user_preferences: Dict[str, Any]) -> float:
            try:
                client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
                response = await client.chat.completions.create(
                    model=settings.GPT_MODEL,
                    messages=[
                        {"role": "system", "content": "Evalúa la relevancia de este documento según las preferencias del usuario."},
                        {"role": "user", "content": f"""
                        Evalúa la relevancia del siguiente contenido:
                        {content}
                        
                        Preferencias del usuario:
                        {user_preferences}
                        
                        Responde con un número entre 0 y 1.
                        """}
                    ],
                    max_tokens=50,
                    temperature=0.1
                )
                
                return float(response.choices[0].message.content)
            except Exception as e:
                raise Exception(f"Error al calcular relevancia: {str(e)}")

        return Tool(
            name="Relevance Scorer",
            description="Calcula la relevancia de un documento",
            func=score_relevance
        )

def extract_keywords(content: str) -> list[str]:
    # Implementar extracción de keywords
    # Por ahora retornamos una lista vacía
    return []

def calculate_relevance(content: str) -> float:
    # Implementar cálculo de relevancia
    # Por ahora retornamos un valor fijo
    return 0.8