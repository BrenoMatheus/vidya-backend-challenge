from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date

from app.core.database import SessionLocal, engine
from app.models.sale_sql import Base
from app.schemas.sale_schema import SaleCreate, SaleResponse
from app.services import sale_service

router = APIRouter(prefix="/sales", tags=["Sales"])

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=SaleResponse)
def create_sale(sale: SaleCreate, db: Session = Depends(get_db)):
    return sale_service.create_sale(db, sale)

@router.get("/", response_model=list[SaleResponse])
def list_sales(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    return sale_service.list_sales(db, start_date, end_date, category)
