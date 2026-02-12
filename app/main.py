from fastapi import FastAPI
from app.routes import health, sales, search

app = FastAPI(title="Sales API")

app.include_router(health.router)
app.include_router(sales.router)
app.include_router(search.router)

