from fastapi import FastAPI
from app.routes import health

app = FastAPI(title="Sales API")

app.include_router(health.router)
