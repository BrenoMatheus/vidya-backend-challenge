from app.models.sale_sql import Sale
from app.schemas.sale_schema import SaleCreate, SaleUpdate
from app.repositories.sale_repository import SaleRepository


class SaleService:
    def __init__(self, repository: SaleRepository):
        self.repository = repository

    def create_sale(self, sale_data: SaleCreate) -> Sale:
        sale = Sale(**sale_data.dict())
        return self.repository.create(sale)

    def list_sales(
        self,
        sale_id=None,
        product_name=None,
        start_date=None,
        end_date=None,
        category=None
    ):
        return self.repository.list(
            sale_id=sale_id,
            product_name=product_name,
            start_date=start_date,
            end_date=end_date,
            category=category
        )
    
    def update_sale(self, sale_id: int, sale_data: SaleUpdate):
        sale = self.repository.get_by_id(sale_id)

        if not sale:
            return None

        for field, value in sale_data.dict(exclude_unset=True).items():
            setattr(sale, field, value)

        return self.repository.update(sale)

    def delete_sale(self, sale_id: int) -> bool:
        sale = self.repository.get_by_id(sale_id)

        if not sale:
            return False

        self.repository.delete(sale)
        return True
