from pydantic import BaseModel
from datetime import date

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
