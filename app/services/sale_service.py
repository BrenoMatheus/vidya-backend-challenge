from app.models.sale_sql import Sale
from app.schemas.sale_schema import SaleCreate
from app.repositories.sale_repository import SaleRepository


class SaleService:
    def __init__(self, repository: SaleRepository):
        self.repository = repository

    def create_sale(self, sale_data: SaleCreate) -> Sale:
        sale = Sale(**sale_data.dict())
        return self.repository.create(sale)

    def list_sales(self, start_date=None, end_date=None, category=None):
        return self.repository.list(start_date, end_date, category)