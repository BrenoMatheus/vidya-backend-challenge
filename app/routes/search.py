from fastapi import APIRouter, Depends
from pymongo.database import Database

from app.schemas.text_schema import TextSearchSchema
from app.repositories.text_repository import TextRepository
from app.services.search_service import SearchService
from app.core.database import get_mongo_db

router = APIRouter(prefix="/search", tags=["Search"])


@router.post("/")
def search_texts(
    payload: TextSearchSchema,
    mongo: Database = Depends(get_mongo_db),
):
    repository = TextRepository(mongo.sale_texts)
    service = SearchService(repository)

    return service.search_texts(
        text=payload.text,
        sale_id=payload.sale_id,
        type=payload.type
    )
