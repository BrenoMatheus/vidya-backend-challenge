from typing import List
from app.repositories.text_repository import TextRepository


class SearchService:
    def __init__(self, repository: TextRepository):
        self.repository = repository

    def search_texts(
        self,
        text: str,
        sale_id: int | None = None,
        type: str | None = None,
        page: int = 1,
        limit: int = 10,
    ):
        page = max(page, 1)
        limit = min(max(limit, 1), 50)
       
        return self.repository.search(
            text=text,
            sale_id=sale_id,
            type=type,
            page=page,
            limit=limit,
        )
