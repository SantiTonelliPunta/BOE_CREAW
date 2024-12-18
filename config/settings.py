from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    BOE_RSS_URL: str = "https://www.boe.es/rss/es"
    OPENAI_API_KEY: str
    GPT_MODEL: str = "gpt-3.5-turbo"
    GPT_MAX_TOKENS: int = 2500
    DATABASE_URL: str
    
    # Parámetros de análisis
    MIN_RELEVANCE_SCORE: float = 0.5
    CACHE_TTL: int = 3600  # 1 hora en segundos
    
    class Config:
        env_file = ".env"

settings = Settings() 