from sqlalchemy.orm import Session
from app.models.sale_sql import Sale
from app.schemas.sale_schema import SaleCreate
from app.repositories import sale_repository

def create_sale(db: Session, sale_data: SaleCreate):
    sale = Sale(**sale_data.dict())
    return sale_repository.create_sale(db, sale)

def list_sales(db: Session, start_date=None, end_date=None, category=None):
    return sale_repository.list_sales(db, start_date, end_date, category)
