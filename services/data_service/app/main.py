from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db import create_db_and_tables
from app.routes.prices import router as price_router
from app.routes.universe import router as universe_router
from app.routes.daily_ohlcv import router as daily_ohlcv_router
from app.routes.intraday_watchlist import router as intraday_watchlist_router
import yaml
from pathlib import Path
import logging.config

config_path = Path(__file__).parent / ".." / "logging.yaml"
with config_path.open("r") as fin:
    config = yaml.safe_load(fin)
    logging.config.dictConfig(config)


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
app.include_router(daily_ohlcv_router, tags = ["daily-ohlcv"])
app.include_router(intraday_watchlist_router, tags=["intraday_watchlist"])

@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8001,
        reload=True,
        log_level="debug",
    )