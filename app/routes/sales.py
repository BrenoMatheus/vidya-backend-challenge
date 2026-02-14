from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date

from app.core.database import get_db, engine
from app.models.sale_sql import Base
from app.schemas.sale_schema import SaleCreate, SaleResponse
from app.repositories.sale_repository import SaleRepository
from app.services.sale_service import SaleService

router = APIRouter(prefix="/sales", tags=["Sales"])

Base.metadata.create_all(bind=engine)


@router.post("/", response_model=SaleResponse)
def create_sale(
    sale: SaleCreate,
    db: Session = Depends(get_db)
):
    repository = SaleRepository(db)
    service = SaleService(repository)

    return service.create_sale(sale)


@router.get("/", response_model=list[SaleResponse])
def list_sales(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    repository = SaleRepository(db)
    service = SaleService(repository)

    return service.list_sales(start_date, end_date, category)
