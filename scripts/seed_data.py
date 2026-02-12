from datetime import date
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, get_mongo_db
from app.models.sale_sql import Sale
from pymongo import MongoClient


def seed_postgres(db: Session):
    sales = [
    # Categoria: Eletrônicos (Alta rotatividade)
    Sale(
        product_name="Notebook Pro",
        category="Eletrônicos",
        quantity=5,
        unit_price=3500.00,
        sale_date=date(2026, 1, 15), # Mês anterior para testar filtros
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

    # Categoria: Eletrodomésticos (Ticket Alto, Baixa quantidade)
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

    # Categoria: Móveis (Para validar o agrupamento)
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
    )
]

    db.add_all(sales)
    db.commit()


def seed_mongo():
    client = MongoClient("mongodb://mongo:27017")
    db = client.sales_db

    db.sale_texts.insert_many([
        # Relacionados ao Notebook (ID 1)
        {
            "sale_id": 1,
            "type": "comment",
            "text": "Cliente muito satisfeito, elogiou a velocidade de processamento e o acabamento em alumínio.",
        },
        {
            "sale_id": 1,
            "type": "observation",
            "text": "Venda realizada com garantia estendida de 2 anos inclusa no pacote.",
        },

        # Relacionados à Geladeira (ID 2)
        {
            "sale_id": 2,
            "type": "description",
            "text": "Modelo Frost Free 450L Inox com tecnologia de economia de energia.",
        },

        # Relacionados ao Fone de Ouvido (ID 3)
        {
            "sale_id": 3,
            "type": "comment",
            "text": "O fone de ouvido é excelente, mas o cabo parece um pouco frágil. Recomendo cuidado.",
        },
        {
            "sale_id": 3,
            "type": "observation",
            "text": "Lote 402 - Verificado selo da Anatel antes do envio.",
        },

        # Cenários de "Problema" ou "Destaque" (Para testar busca textual)
        {
            "sale_id": 4, # Cadeira Ergonômica
            "type": "comment",
            "text": "A caixa chegou com um pequeno rasgo, mas o produto estava intacto.",
        },
        {
            "sale_id": 6, # Mouse Gamer
            "type": "description",
            "text": "Sensor óptico de 16000 DPI. Acompanha conjunto de pesos extras.",
        }
    ])


if __name__ == "__main__":
    db = SessionLocal()
    seed_postgres(db)
    seed_mongo()
    db.close()

    print("✅ Seed executado com sucesso")
