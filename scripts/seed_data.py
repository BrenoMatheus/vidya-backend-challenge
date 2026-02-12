from datetime import date
from sqlalchemy.orm import Session
from pymongo import MongoClient

from app.core.database import SessionLocal
from app.models.sale_sql import Sale


# ---------- POSTGRES ----------
def seed_postgres(db: Session):
    sales = [
        Sale(
            product_name="Notebook Pro",
            category="Eletrônicos",
            quantity=5,
            unit_price=3500.00,
            sale_date=date(2026, 1, 15),
        ),
        Sale(
            product_name="Fone de Ouvido Bluetooth",
            category="Eletrônicos",
            quantity=40,
            unit_price=150.00,
            sale_date=date(2026, 2, 10),
        ),
        Sale(
            product_name="Mouse Gamer",
            category="Eletrônicos",
            quantity=15,
            unit_price=250.00,
            sale_date=date(2026, 2, 12),
        ),
        Sale(
            product_name="Geladeira Frost Free",
            category="Eletrodomésticos",
            quantity=2,
            unit_price=4200.00,
            sale_date=date(2026, 2, 5),
        ),
        Sale(
            product_name="Micro-ondas 30L",
            category="Eletrodomésticos",
            quantity=8,
            unit_price=800.00,
            sale_date=date(2026, 2, 8),
        ),
        Sale(
            product_name="Cadeira Ergonômica",
            category="Móveis",
            quantity=10,
            unit_price=1200.00,
            sale_date=date(2026, 2, 11),
        ),
        Sale(
            product_name="Mesa de Escritório",
            category="Móveis",
            quantity=4,
            unit_price=950.00,
            sale_date=date(2026, 2, 12),
        ),
    ]

    db.add_all(sales)
    db.commit()


# ---------- MONGO ----------
def seed_mongo():
    client = MongoClient("mongodb://mongo:27017")

    db = client.sales_texts
    collection = db.sale_texts


    collection.insert_many([
        {
            "sale_id": 1,
            "type": "comment",
            "text": "Cliente muito satisfeito, elogiou a velocidade e o acabamento.",
        },
        {
            "sale_id": 1,
            "type": "observation",
            "text": "Venda realizada com garantia estendida de 2 anos.",
        },
        {
            "sale_id": 2,
            "type": "description",
            "text": "Modelo Frost Free 450L Inox com economia de energia.",
        },
        {
            "sale_id": 3,
            "type": "comment",
            "text": "Produto excelente, porém embalagem poderia ser melhor.",
        },
        {
            "sale_id": 4,
            "type": "comment",
            "text": "Caixa com pequeno dano, mas produto intacto.",
        },
    ])


if __name__ == "__main__":
    db = SessionLocal()
    seed_postgres(db)
    seed_mongo()
    db.close()

    print("✅ Seed executado com sucesso")
