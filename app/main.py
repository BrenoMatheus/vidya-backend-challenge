from fastapi import FastAPI
from app.routes import health, sales, search, texts, analytics

app = FastAPI(title="Sales API")

app.include_router(health.router)
app.include_router(sales.router)
app.include_router(search.router)
app.include_router(texts.router)
app.include_router(analytics.router)