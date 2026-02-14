from typing import Optional, Dict, Any
from app.repositories.text_repository import TextRepository
from app.repositories.sale_repository import SaleRepository


class SearchService:
    def __init__(
        self,
        text_repository: TextRepository,
        sale_repository: SaleRepository,
    ):
        self.text_repository = text_repository
        self.sale_repository = sale_repository

    def search(
        self,
        text: str,
        sale_id: Optional[int] = None,
        type: Optional[str] = None,
        page: int = 1,
        limit: int = 10,
    ) -> Dict[str, Any]:

        mongo_result = self.text_repository.search(
            text=text,
            sale_id=sale_id,
            type=type,
            page=page,
            limit=limit,
        )

        items = mongo_result["items"]

        sale_ids = list({item["sale_id"] for item in items if "sale_id" in item})

        sales = self.sale_repository.list_by_ids(
            sale_ids=sale_ids,
            offset=0,
            limit=limit,
        )

        sales_map = {sale.id: sale for sale in sales}

        result = []
        for item in items:
            sale = sales_map.get(item["sale_id"])
            if sale:
                result.append({
                    "sale": sale,
                    "id": item.get("id"),
                    "text": item.get("text"),
                    "score": item.get("score"),
                    "type": item.get("type"),
                })

        return {
            "items": result,
            "meta": mongo_result["meta"],
        }
