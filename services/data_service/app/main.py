from fastapi import FastAPI
from .routes import prices
from app.services.data_store import init_db

app = FastAPI(
    title="Data Service",
    description="Provides market data to other services in the quant_management_platform",
    version="0.1.0",
)

@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}

# Include routers
app.include_router(prices.router, prefix="/prices", tags=["prices"])

# Init Database
init_db()