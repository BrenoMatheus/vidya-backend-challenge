from pydantic import BaseModel


class RevenueByCategorySchema(BaseModel):
    category: str
    revenue: float
    quantity: int
    average_ticket: float
