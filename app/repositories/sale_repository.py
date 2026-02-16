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

    def list(self,sale_id=None, product_name=None, start_date=None, end_date=None, category=None):
        query = self.db.query(Sale)

        if sale_id:
            query = query.filter(Sale.id == sale_id)
        if product_name:
            query = query.filter(Sale.product_name.ilike(f"%{product_name}%"))
        if start_date:
            query = query.filter(Sale.sale_date >= start_date)
        if end_date:
            query = query.filter(Sale.sale_date <= end_date)
        if category:
            query = query.filter(Sale.category == category)

        return query.all()
    
    def update(self, sale: Sale):
        self.db.commit()
        self.db.refresh(sale)
        return sale

    def delete(self, sale: Sale):
        self.db.delete(sale)
        self.db.commit()

    def get_by_id(self, sale_id: int):
        return self.db.query(Sale).filter(Sale.id == sale_id).first()

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
