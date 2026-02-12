from sqlalchemy import Column, Integer, String, Date, Numeric
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    sale_date = Column(Date, nullable=False)
