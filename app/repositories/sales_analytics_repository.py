from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.sale import Sale


class SalesAnalyticsRepository:
    def __init__(self, db: Session):
        self.db = db

    def revenue_by_category(self):
        return (
            self.db.query(
                Sale.category.label("category"),
                func.sum(Sale.quantity * Sale.unit_price).label("revenue"),
                func.sum(Sale.quantity).label("quantity"),
            )
            .group_by(Sale.category)
            .all()
        )
