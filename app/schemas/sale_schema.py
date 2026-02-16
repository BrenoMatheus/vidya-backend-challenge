from pydantic import BaseModel
from typing import Optional
from datetime import date

class SaleUpdate(BaseModel):
    product_name: Optional[str]
    category: Optional[str]
    quantity: Optional[int]
    unit_price: Optional[float]
    sale_date: Optional[date]

class SaleCreate(BaseModel):
    product_name: str
    category: str
    quantity: int
    unit_price: float
    sale_date: date

class SaleResponse(SaleCreate):
    id: int

    class Config:
        from_attributes = True
