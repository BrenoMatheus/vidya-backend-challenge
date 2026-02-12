from bson import ObjectId
from datetime import datetime


class TextRepository:
    def __init__(self, collection):
        self.collection = collection

    def _normalize(self, doc: dict) -> dict:
        doc["id"] = str(doc.pop("_id"))
        return doc

    def search(
            self,
            text: str,
            sale_id=None,
            type=None,
            page: int = 1,
            limit: int = 10,
        ):
            query = {"$text": {"$search": text}}

            if sale_id is not None:
                query["sale_id"] = sale_id

            if type is not None:
                query["type"] = type

            skip = (page - 1) * limit

            cursor = (
                self.collection
                .find(query, {"score": {"$meta": "textScore"}})
                .sort([("score", {"$meta": "textScore"})])
                .skip(skip)
                .limit(limit)
            )

            total = self.collection.count_documents(query)

            return {
                "items": [self._normalize(doc) for doc in cursor],
                "meta": {
                    "page": page,
                    "limit": limit,
                    "total": total,
                    "pages": (total + limit - 1) // limit,
                },
            }
    
    def create(self, data: dict) -> dict:
        data["created_at"] = datetime.utcnow()
        result = self.collection.insert_one(data)

        created = self.collection.find_one({"_id": result.inserted_id})
        return self._normalize(created)
