from bson import ObjectId
from datetime import datetime


class TextRepository:
    def __init__(self, collection):
        self.collection = collection

    def _normalize(self, doc: dict) -> dict:
        doc["id"] = str(doc.pop("_id"))
        return doc

    def search(self, text: str, sale_id=None, type=None):
        query = {"$text": {"$search": text}}

        if sale_id is not None:
            query["sale_id"] = sale_id

        if type is not None:
            query["type"] = type

        cursor = self.collection.find(
            query,
            {"score": {"$meta": "textScore"}}
        ).sort(
            [("score", {"$meta": "textScore"})]
        )

        return [self._normalize(doc) for doc in cursor]
    
    def create(self, data: dict) -> dict:
        data["created_at"] = datetime.utcnow()
        result = self.collection.insert_one(data)

        created = self.collection.find_one({"_id": result.inserted_id})
        return self._normalize(created)
