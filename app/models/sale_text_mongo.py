from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field


class SaleTextMongo(BaseModel):
    sale_id: int
    type: Literal["comment", "observation", "description"]
    text: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
