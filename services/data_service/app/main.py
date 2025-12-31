from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db import create_db_and_tables
from app.routes.prices import router as price_router
from app.routes.universe import router as universe_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(
    title="Data Service",
    description="Provides market data to other services in the quant_management_platform",
    version="0.1.0",
    lifespan=lifespan
)
# Include routers
app.include_router(price_router, tags=["prices"])
app.include_router(universe_router, tags=["universe"])

@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}

