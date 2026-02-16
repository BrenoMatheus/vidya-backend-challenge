from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date

from app.core.database import get_db, engine
from app.models.sale_sql import Base
from app.schemas.sale_schema import SaleCreate, SaleResponse, SaleUpdate
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
    id: Optional[int] = Query(None),
    product_name: Optional[str] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    service = SaleService(SaleRepository(db))
    return service.list_sales(
        sale_id=id,
        product_name=product_name,
        start_date=start_date,
        end_date=end_date,
        category=category
    )

@router.put("/{sale_id}", response_model=SaleResponse)
def update_sale(
    sale_id: int,
    sale: SaleUpdate,
    db: Session = Depends(get_db)
):
    service = SaleService(SaleRepository(db))
    updated_sale = service.update_sale(sale_id, sale)

    if not updated_sale:
        raise HTTPException(status_code=404, detail="Sale not found")

    return updated_sale


@router.delete("/{sale_id}", status_code=204)
def delete_sale(
    sale_id: int,
    db: Session = Depends(get_db)
):
    service = SaleService(SaleRepository(db))
    deleted = service.delete_sale(sale_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Sale not found")