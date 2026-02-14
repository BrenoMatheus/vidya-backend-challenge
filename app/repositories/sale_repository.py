from sqlalchemy.orm import Session
from app.models.sale_sql import Sale
from typing import List


class SaleRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, sale: Sale) -> Sale:
        self.db.add(sale)
        self.db.commit()
        self.db.refresh(sale)
        return sale

    def list(self, start_date=None, end_date=None, category=None):
        query = self.db.query(Sale)

        if start_date:
            query = query.filter(Sale.sale_date >= start_date)
        if end_date:
            query = query.filter(Sale.sale_date <= end_date)
        if category:
            query = query.filter(Sale.category == category)

        return query.all()

    def list_by_ids(
        self,
        sale_ids: List[int],
        offset: int = 0,
        limit: int = 10,
    ):
        if not sale_ids:
            return []

        return (
            self.db.query(Sale)
            .filter(Sale.id.in_(sale_ids))
            .offset(offset)
            .limit(limit)
            .all()
        )
