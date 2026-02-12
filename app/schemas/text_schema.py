from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class TextCreateSchema(BaseModel):
    sale_id: int
    type: str
    text: str


class TextSearchSchema(BaseModel):
    text: str
    sale_id: Optional[int] = None
    type: Optional[str] = None


class TextResponseSchema(BaseModel):
    id: str
    sale_id: int
    type: str
    text: str
    created_at: datetime
