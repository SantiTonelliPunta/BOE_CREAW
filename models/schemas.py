from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class BOEEntry(BaseModel):
    id: str
    content: str
    metadata: dict
    processed_at: datetime
    
class AnalyzedContent(BaseModel):
    entry_id: str
    summary: str
    keywords: List[str]
    relevance_score: float
    
class Report(BaseModel):
    content_id: str
    summary: str
    recipients: List[str]
    sent_at: Optional[datetime] 