from fastapi import APIRouter, Depends, HTTPException
from pymongo.database import Database

from app.schemas.text_schema import TextCreateSchema, TextResponseSchema
from app.repositories.text_repository import TextRepository
from app.services.text_service import TextService
from app.core.database import get_mongo_db

router = APIRouter(prefix="/texts", tags=["Texts"])


@router.post("/", response_model=TextResponseSchema)
def create_text(
    payload: TextCreateSchema,
    mongo: Database = Depends(get_mongo_db),
):
    repository = TextRepository(mongo.sale_texts)
    service = TextService(repository)

    try:
        return service.create_text(payload.dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
