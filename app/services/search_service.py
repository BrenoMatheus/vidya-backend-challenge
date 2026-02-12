from typing import List
from app.repositories.text_repository import TextRepository


class SearchService:
    def __init__(self, repository: TextRepository):
        self.repository = repository

    def search_texts(
        self,
        text: str,
        sale_id: int | None = None,
        type: str | None = None
    ) -> List[dict]:
        if not text.strip():
            raise ValueError("Texto de busca não pode ser vazio")

        return self.repository.search(
            text=text,
            sale_id=sale_id,
            type=type
        )
