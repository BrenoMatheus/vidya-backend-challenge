from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pymongo.database import Database

from app.schemas.text_schema import TextSearchSchema
from app.repositories.text_repository import TextRepository
from app.repositories.sale_repository import SaleRepository
from app.services.search_service import SearchService
from app.core.database import get_mongo_db, get_db

router = APIRouter(prefix="/search", tags=["Search"])

@router.post("/")
def search_texts(
    payload: TextSearchSchema,
    page: int = 1,
    limit: int = 10,
    mongo: Database = Depends(get_mongo_db),
    db: Session = Depends(get_db),
):
    text_repository = TextRepository(mongo.sale_texts)
    sale_repository = SaleRepository(db)

    service = SearchService(
        text_repository=text_repository,
        sale_repository=sale_repository,
    )

    return service.search(
        text=payload.text,
        sale_id=payload.sale_id,
        type=payload.type,
        page=page,
        limit=limit,
    )
