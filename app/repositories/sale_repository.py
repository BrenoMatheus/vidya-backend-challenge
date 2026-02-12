from sqlalchemy.orm import Session
from app.models.sale_sql import Sale

def create_sale(db: Session, sale: Sale):
    db.add(sale)
    db.commit()
    db.refresh(sale)
    return sale

def list_sales(db: Session, start_date=None, end_date=None, category=None):
    query = db.query(Sale)

    if start_date:
        query = query.filter(Sale.sale_date >= start_date)
    if end_date:
        query = query.filter(Sale.sale_date <= end_date)
    if category:
        query = query.filter(Sale.category == category)

    return query.all()
