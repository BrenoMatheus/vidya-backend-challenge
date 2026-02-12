from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.sales_analytics_repository import SalesAnalyticsRepository
from app.services.sales_analytics_service import SalesAnalyticsService
from app.schemas.analytics_schema import RevenueByCategorySchema

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get(
    "/by-category",
    response_model=list[RevenueByCategorySchema],
)
def revenue_by_category(db: Session = Depends(get_db)):
    repository = SalesAnalyticsRepository(db)
    service = SalesAnalyticsService(repository)

    return service.revenue_by_category()
